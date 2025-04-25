import bisect
import itertools
import operator
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator, Mapping, Set
from dataclasses import InitVar, dataclass, field
from decimal import Decimal
from enum import StrEnum
from random import Random
from typing import Any

from apischema import deserializer, serializer
from apischema.conversions import Conversion
from lark import Token
from lark.tree import Meta


class Location(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class FileLocation(Location):
    line: int
    column: int

    def __post_init__(self) -> None:
        if self.line <= 0:
            raise ValueError(
                f"line number must be positive, is instead {self.line}"
            )

        if self.column <= 0:
            raise ValueError(
                f"column number must be positive, is instead {self.column}"
            )

    @classmethod
    def from_meta(cls, meta: Meta) -> "FileLocation":
        return FileLocation(meta.line, meta.column)

    @classmethod
    def from_token(cls, token: Token) -> "FileLocation":
        if not token.line:
            raise ValueError("token must have line information")

        if not token.column:
            raise ValueError("token must have column information")

        return FileLocation(token.line, token.column)

    def __str__(self) -> str:
        return f"{self.line}:{self.column}"


@dataclass(frozen=True)
class EmptyLocation(Location):
    def __str__(self) -> str:
        return "?:?"


@dataclass(frozen=True, eq=True)
class Locationed[T]:
    value: T
    location: Location = field(
        hash=False, compare=False, default=EmptyLocation()
    )

    @serializer
    def _serialize(self) -> T:
        return self.value

    def __str__(self) -> str:
        return f"{self.value} ({self.location})"


deserializer(Locationed)


class Requirement(StrEnum):
    STRIPS = ":strips"
    TYPING = ":typing"
    DISJUNCTIVE_PRECONDITIONS = ":disjunctive-preconditions"
    EQUALITY = ":equality"
    PROBABILISTIC_EFFECTS = ":probabilistic-effects"


@dataclass(frozen=True)
class Identifier:
    value: str

    def __str__(self) -> str:
        return self.value

    @serializer
    def _serialize(self) -> str:
        return self.value

    @classmethod
    def deserialize[I: Identifier](cls: type[I], value: str) -> I:
        return cls(value)

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        deserializer(Conversion(cls.deserialize, target=cls))


deserializer(Conversion(Identifier.deserialize, target=Identifier))


@dataclass(frozen=True)
class Variable(Identifier):
    def __str__(self) -> str:
        return f"?{self.value}"


@dataclass(frozen=True)
class CustomType(Identifier):
    pass


@dataclass(eq=True, frozen=True)
class ObjectType:
    def __str__(self) -> str:
        return "object"


type Type = CustomType | ObjectType


@dataclass(frozen=True)
class Object(Identifier):
    pass


@dataclass(eq=True, frozen=True)
class Typed[T]:
    value: T
    type: Locationed[Type]


@dataclass(frozen=True)
class TypeHierarchy:
    _supertypes: Mapping[Locationed[CustomType], Locationed[Type]]

    @classmethod
    def from_raw_parts(
        cls, custom_types: Iterable[Typed[Locationed[CustomType]]]
    ) -> "TypeHierarchy":
        supertypes = {}

        for custom_type in custom_types:
            if custom_type.value in supertypes:
                raise ValueError(
                    f"type '{custom_type.value}' is defined multiple times"
                )

            supertypes[custom_type.value] = custom_type.type

        return TypeHierarchy(supertypes)

    def __iter__(self) -> Iterator[Typed[Locationed[CustomType]]]:
        return (
            Typed(subtype, supertype)
            for subtype, supertype in self._supertypes.items()
        )

    def supertype(
        self, custom_type: Locationed[CustomType]
    ) -> Locationed[Type]:
        return self._supertypes[custom_type]

    def is_compatible(
        self, test_type: Locationed[Type], tester_type: Locationed[Type]
    ) -> bool:
        # Technically speaking `is_compatible` implements the transitive closure
        # of a DAG. Usually this DAG is fairly shallow, and so performance
        # should be fine. Still, this could use some work.
        if test_type == tester_type:
            return True
        elif isinstance(test_type, CustomType):
            return self.is_compatible(self.supertype(test_type), tester_type)
        else:
            return False

    def __contains__(self, item: Any) -> bool:
        return item in self._supertypes


@dataclass(frozen=True)
class PredicateDefinition:
    name: Locationed[Identifier]
    parameters: list[Typed[Locationed[Variable]]]

    @classmethod
    def from_raw_parts(
        cls,
        name: Locationed[Identifier],
        parameters: list[Typed[Locationed[Variable]]],
    ) -> "PredicateDefinition":
        variables = set()

        for parameter in parameters:
            if parameter.value in variables:
                raise ValueError(
                    f"parameter '{parameter.value}' of predicate definition '{name}' defined multiple times"  # noqa: E501
                )

            variables.add(parameter.value)

        return PredicateDefinition(name, parameters)

    def _validate(self, type_hierarchy: Locationed[TypeHierarchy]) -> None:
        for parameter in self.parameters:
            if (
                isinstance(parameter.type.value, CustomType)
                and parameter.type not in type_hierarchy.value
            ):
                raise ValueError(
                    f"parameter '{parameter.value}' of predicate definition '{self.name}' uses an undefined type: '{parameter.type}'"  # noqa: E501
                )


type Argument = Variable | Object


@dataclass(frozen=True)
class AndCondition[A: Argument]:
    subconditions: list[Locationed["Condition[A]"]]

    def _validate(
        self,
        _location: Location,
        variable_types: Mapping[Locationed[Variable], Locationed[Type]],
        object_types: Mapping[Locationed[Object], Locationed[Type]],
        predicate_definitions: Mapping[
            Locationed[Identifier], PredicateDefinition
        ],
        type_hierarchy: Locationed[TypeHierarchy],
        requirements: Locationed[Set[Requirement]],
    ) -> None:
        for subcondition in self.subconditions:
            subcondition.value._validate(
                subcondition.location,
                variable_types,
                object_types,
                predicate_definitions,
                type_hierarchy,
                requirements,
            )


@dataclass(frozen=True)
class OrCondition[A: Argument]:
    subconditions: list[Locationed["Condition[A]"]]

    def _validate(
        self,
        location: Location,
        variable_types: Mapping[Locationed[Variable], Locationed[Type]],
        object_types: Mapping[Locationed[Object], Locationed[Type]],
        predicate_definitions: Mapping[
            Locationed[Identifier], PredicateDefinition
        ],
        type_hierarchy: Locationed[TypeHierarchy],
        requirements: Locationed[Set[Requirement]],
    ) -> None:
        if Requirement.DISJUNCTIVE_PRECONDITIONS not in requirements.value:
            disjunction_text = Locationed("disjunction", location)

            raise ValueError(
                f"{disjunction_text} used in condition, but '{Requirement.DISJUNCTIVE_PRECONDITIONS}' is not used"  # noqa: E501
            )

        for subcondition in self.subconditions:
            subcondition.value._validate(
                subcondition.location,
                variable_types,
                object_types,
                predicate_definitions,
                type_hierarchy,
                requirements,
            )


@dataclass(frozen=True)
class NotCondition[A: Argument]:
    base_condition: "Locationed[Condition[A]]"

    def _validate(
        self,
        _location: Location,
        variable_types: Mapping[Locationed[Variable], Locationed[Type]],
        object_types: Mapping[Locationed[Object], Locationed[Type]],
        predicate_definitions: Mapping[
            Locationed[Identifier], PredicateDefinition
        ],
        type_hierarchy: Locationed[TypeHierarchy],
        requirements: Locationed[Set[Requirement]],
    ) -> None:
        self.base_condition.value._validate(
            self.base_condition.location,
            variable_types,
            object_types,
            predicate_definitions,
            type_hierarchy,
            requirements,
        )


@dataclass(frozen=True)
class EqualityCondition[A: Argument]:
    left_side: Locationed[A]
    right_side: Locationed[A]

    def __str__(self) -> str:
        return f"(= {self.left_side.value} {self.right_side.value})"

    def _validate(
        self,
        location: Location,
        variable_types: Mapping[Locationed[Variable], Locationed[Type]],
        object_types: Mapping[Locationed[Object], Locationed[Type]],
        _predicate_definitions: Mapping[
            Locationed[Identifier], PredicateDefinition
        ],
        _type_hierarchy: Locationed[TypeHierarchy],
        requirements: Locationed[Set[Requirement]],
    ) -> None:
        if Requirement.EQUALITY not in requirements.value:
            equality_predicate_text = Locationed("equality predicate", location)

            raise ValueError(
                f"{equality_predicate_text} used in condition, but '{Requirement.EQUALITY}' is not used"  # noqa: E501
            )

        def validate_argument(argument: Locationed[A]) -> None:
            match argument.value:
                case Variable():
                    if argument not in variable_types:
                        raise ValueError(f"variable '{argument}' is undefined")
                case Object():
                    if argument not in object_types:
                        raise ValueError(f"constant '{argument}' is undefined")

        validate_argument(self.left_side)
        validate_argument(self.right_side)


@dataclass(frozen=True)
class Predicate[A: Argument]:
    name: Locationed[Identifier]
    assignment: tuple[Locationed[A], ...]

    def __str__(self) -> str:
        result = f"({self.name}"

        for argument in self.assignment:
            result += f" {argument}"

        result += ")"

        return result

    def _validate(
        self,
        _location: Location,
        variable_types: Mapping[Locationed[Variable], Locationed[Type]],
        object_types: Mapping[Locationed[Object], Locationed[Type]],
        predicate_definitions: Mapping[
            Locationed[Identifier], PredicateDefinition
        ],
        type_hierarchy: Locationed[TypeHierarchy],
        _requirements: Locationed[Set[Requirement]],
    ) -> None:
        if self.name not in predicate_definitions:
            raise ValueError(f"predicate {self.name} is undefined")

        predicate_definition = predicate_definitions[self.name]

        for parameter, argument in zip(
            predicate_definition.parameters, self.assignment, strict=True
        ):
            match argument.value:
                case Variable():
                    if argument not in variable_types:
                        raise ValueError(f"variable '{argument}' is undefined")

                    argument_type = variable_types[argument]  # type: ignore
                case Object():
                    if argument not in object_types:
                        raise ValueError(f"constant '{argument}' is undefined")

                    argument_type = object_types[argument]  # type: ignore

            if not type_hierarchy.value.is_compatible(
                argument_type, parameter.type
            ):
                raise ValueError(
                    f"parameter '{parameter.value}' of predicate '{self.name}' is of type '{parameter.type}', but is assigned argument '{argument}' of incompatible type '{argument_type}'"  # noqa: E501
                )


type Condition[A: Argument] = (
    AndCondition[A]
    | OrCondition[A]
    | NotCondition[A]
    | EqualityCondition[A]
    | Predicate[A]
)


@dataclass(frozen=True)
class NotPredicate[A: Argument]:
    base_predicate: Locationed[Predicate[A]]

    def _validate(
        self,
        _location: Location,
        variable_types: Mapping[Locationed[Variable], Locationed[Type]],
        object_types: Mapping[Locationed[Object], Locationed[Type]],
        predicate_definitions: Mapping[
            Locationed[Identifier], PredicateDefinition
        ],
        type_hierarchy: Locationed[TypeHierarchy],
        requirements: Locationed[Set[Requirement]],
    ) -> None:
        self.base_predicate.value._validate(
            self.base_predicate.location,
            variable_types,
            object_types,
            predicate_definitions,
            type_hierarchy,
            requirements,
        )


type Atom[A: Argument] = Predicate[A] | NotPredicate[A]


@dataclass(frozen=True)
class AndEffect[A: Argument]:
    subeffects: list[Locationed["Effect[A]"]]

    def _validate(
        self,
        _location: Location,
        variable_types: Mapping[Locationed[Variable], Locationed[Type]],
        object_types: Mapping[Locationed[Object], Locationed[Type]],
        predicate_definitions: Mapping[
            Locationed[Identifier], PredicateDefinition
        ],
        type_hierarchy: Locationed[TypeHierarchy],
        requirements: Locationed[Set[Requirement]],
    ) -> None:
        for subeffect in self.subeffects:
            subeffect.value._validate(
                subeffect.location,
                variable_types,
                object_types,
                predicate_definitions,
                type_hierarchy,
                requirements,
            )


@dataclass(frozen=True)
class ProbabilisticEffect[A: Argument]:
    _possible_effects: list[Locationed["Effect[A]"]]
    _cummulative_probabilities: list[Decimal]

    @classmethod
    def from_possibilities(
        cls, possibilities: list[tuple[Decimal, Locationed["Effect[A]"]]]
    ) -> "ProbabilisticEffect":
        possible_effects = [possibility for _, possibility in possibilities]
        cummulative_probabilities = list(
            itertools.accumulate(
                (probability for probability, _ in possibilities), operator.add
            )
        )

        total_probability = cummulative_probabilities[-1]

        if total_probability > 1:
            raise ValueError(
                "total probability mustn't be greater than 1"
                f", is {total_probability}"
            )

        return ProbabilisticEffect(possible_effects, cummulative_probabilities)

    def choose_possibility(self, rng: Random) -> Locationed["Effect[A]"]:
        index = bisect.bisect(self._cummulative_probabilities, rng.random())

        if index == len(self._possible_effects):
            return Locationed(AndEffect([]))  # Empty effect

        return self._possible_effects[index]

    def _validate(
        self,
        location: Location,
        variable_types: Mapping[Locationed[Variable], Locationed[Type]],
        object_types: Mapping[Locationed[Object], Locationed[Type]],
        predicate_definitions: Mapping[
            Locationed[Identifier], PredicateDefinition
        ],
        type_hierarchy: Locationed[TypeHierarchy],
        requirements: Locationed[Set[Requirement]],
    ) -> None:
        if Requirement.PROBABILISTIC_EFFECTS not in requirements.value:
            probabilistic_effect_text = Locationed(
                "probabilistic effect", location
            )

            raise ValueError(
                f"{probabilistic_effect_text} used in action, but '{Requirement.PROBABILISTIC_EFFECTS}' is not used"  # noqa: E501
            )

        for effect in self._possible_effects:
            effect.value._validate(
                effect.location,
                variable_types,
                object_types,
                predicate_definitions,
                type_hierarchy,
                requirements,
            )


type Effect[A: Argument] = AndEffect[A] | ProbabilisticEffect[A] | Atom[A]


@dataclass(frozen=True)
class ActionDefinition:
    name: Locationed[Identifier]
    variable_types: dict[Locationed[Variable], Locationed[Type]]
    precondition: Locationed[Condition[Argument]]
    effect: Locationed[Effect[Argument]]

    @classmethod
    def from_raw_parts(
        cls,
        name: Locationed[Identifier],
        parameters: list[Typed[Locationed[Variable]]],
        precondition: Locationed[Condition[Argument]],
        effect: Locationed[Effect[Argument]],
    ) -> "ActionDefinition":
        variable_types = {}

        for parameter in parameters:
            if parameter.value in variable_types:
                raise ValueError(
                    f"parameter '{parameter.value}' of action definition '{name}' defined multiple times"  # noqa: E501
                )

            # The dictionary is insertion ordered, so this is fine
            variable_types[parameter.value] = parameter.type

        return ActionDefinition(name, variable_types, precondition, effect)

    def _validate(
        self,
        constant_types: Mapping[Locationed[Object], Locationed[Type]],
        predicate_definitions: Mapping[
            Locationed[Identifier], PredicateDefinition
        ],
        type_hierarchy: Locationed[TypeHierarchy],
        requirements: Locationed[Set[Requirement]],
    ) -> None:
        # The dictionary is insertion ordered, so this is fine
        for variable, type in self.variable_types.items():
            if (
                isinstance(type.value, CustomType)
                and type not in type_hierarchy.value
            ):
                raise ValueError(
                    f"parameter '{variable}' of action definition '{self.name}' uses an undefined type: '{type}'"  # noqa: E501
                )

        self.precondition.value._validate(
            self.precondition.location,
            self.variable_types,
            constant_types,
            predicate_definitions,
            type_hierarchy,
            requirements,
        )
        self.effect.value._validate(
            self.effect.location,
            self.variable_types,
            constant_types,
            predicate_definitions,
            type_hierarchy,
            requirements,
        )


@dataclass(frozen=True)
class Domain:
    name: Locationed[Identifier]
    requirements: Locationed[Set[Requirement]]
    type_hierarchy: Locationed[TypeHierarchy] = field(init=False)
    _type_hierarchy: InitVar[Locationed[TypeHierarchy] | None]
    constant_types: Mapping[Locationed[Object], Locationed[Type]]
    predicate_definitions: Mapping[Locationed[Identifier], PredicateDefinition]
    action_definitions: Mapping[Locationed[Identifier], ActionDefinition]

    @classmethod
    def from_raw_parts(
        cls,
        name: Locationed[Identifier],
        requirements: Locationed[Iterable[Requirement]],
        type_hierarchy: Locationed[TypeHierarchy] | None,
        constants: Iterable[Typed[Locationed[Object]]],
        predicate_definitions: Iterable[PredicateDefinition],
        action_definitions: Iterable[ActionDefinition],
    ) -> "Domain":
        requirements_set = set()

        for requirement in requirements.value:
            if requirement in requirements_set:
                requirements_text = Locationed(
                    "requirements", requirements.location
                )

                raise ValueError(
                    f"requirement '{requirement}' appears multiple times in {requirements_text}"  # noqa: E501
                )

            requirements_set.add(requirement)

        constant_types = {}

        for constant in constants:
            if constant.value in constant_types:
                raise ValueError(
                    f"constant '{constant.value}' defined multiple times"
                )

            constant_types[constant.value] = constant.type

        predicate_definition_map = {}

        for predicate_definition in predicate_definitions:
            if predicate_definition.name in predicate_definition_map:
                raise ValueError(
                    f"predicate '{predicate_definition.name}' is defined multiple times"  # noqa: E501
                )

            predicate_definition_map[predicate_definition.name] = (
                predicate_definition
            )

        action_definition_map = {}

        for action_definition in action_definitions:
            if action_definition.name in action_definition_map:
                raise ValueError(
                    f"action '{action_definition.name}' is defined multiple times"  # noqa: E501
                )

            action_definition_map[action_definition.name] = action_definition
        return Domain(
            name,
            Locationed(requirements_set, requirements.location),
            type_hierarchy,
            constant_types,
            predicate_definition_map,
            action_definition_map,
        )

    def __post_init__(
        self, type_hierarchy: Locationed[TypeHierarchy] | None
    ) -> None:
        object.__setattr__(
            self,
            "type_hierarchy",
            type_hierarchy if type_hierarchy else Locationed(TypeHierarchy({})),
        )
        self._validate(type_hierarchy)

    def _validate_type_hierarchy(
        self, type_hierarchy: Locationed[TypeHierarchy] | None
    ) -> None:
        if (
            Requirement.TYPING not in self.requirements.value
            and type_hierarchy is not None
        ):
            types_text = Locationed("types", type_hierarchy.location)

            raise ValueError(
                f"{types_text} are defined in domain, but '{Requirement.TYPING}' requirement is not used"  # noqa: E501
            )

    def _validate_constant_types(self) -> None:
        for constant, type in self.constant_types.items():
            if (
                isinstance(type.value, CustomType)
                and type not in self.type_hierarchy.value
            ):
                raise ValueError(
                    f"constant '{constant}' has type {type}, but that type is undefined"  # noqa: E501
                )

    def _validate_predicate_definitions(self) -> None:
        for predicate_definition in self.predicate_definitions.values():
            predicate_definition._validate(self.type_hierarchy)

    def _validate_action_definitions(self) -> None:
        for action_definition in self.action_definitions.values():
            action_definition._validate(
                self.constant_types,
                self.predicate_definitions,
                self.type_hierarchy,
                self.requirements,
            )

    def _validate(
        self, type_hierarchy: Locationed[TypeHierarchy] | None
    ) -> None:
        self._validate_type_hierarchy(type_hierarchy)
        self._validate_constant_types()
        self._validate_predicate_definitions()
        self._validate_action_definitions()


@dataclass(frozen=True)
class RawProblemParts:
    name: Locationed[Identifier]
    used_domain_name: Locationed[Identifier]
    objects: list[Typed[Locationed[Object]]]
    initialization: list[Locationed[Predicate[Object]]]
    goal_condition: Locationed[Condition[Object]]


@dataclass(frozen=True)
class Problem:
    name: Locationed[Identifier]
    used_domain_name: Locationed[Identifier]
    object_types: Mapping[Locationed[Object], Locationed[Type]]
    initialization: Set[Locationed[Predicate[Object]]]
    goal_condition: Locationed[Condition[Object]]
    domain: InitVar[Domain]

    @classmethod
    def from_raw_parts(
        cls,
        raw_parts: RawProblemParts,
        domain: Domain,
    ) -> "Problem":
        object_types = {}

        for object_ in raw_parts.objects:
            if object_.value in object_types:
                raise ValueError(
                    f"object '{object_.value}' is defined multiple times"
                )

            object_types[object_.value] = object_.type

        true_predicates = set()

        for predicate in raw_parts.initialization:
            if predicate in true_predicates:
                raise ValueError(
                    f"predicate '{predicate}' appears in initialization multiple times"  # noqa: E501
                )

            true_predicates.add(predicate)

        return Problem(
            raw_parts.name,
            raw_parts.used_domain_name,
            object_types,
            true_predicates,
            raw_parts.goal_condition,
            domain,
        )

    def __post_init__(self, domain: Domain) -> None:
        self._validate(domain)

    def _validate_used_domain_name(self, domain: Domain) -> None:
        if domain.name != self.used_domain_name:
            raise ValueError(
                f"used domain name '{self.used_domain_name}' doesn't match paired domain name '{domain.name}'"  # noqa: E501
            )

    def _validate_object_types(self, domain: Domain) -> None:
        for object_, type in self.object_types.items():
            if type not in domain.type_hierarchy.value:
                raise ValueError(
                    f"object '{object_}' is of non-existent type: '{type}'"
                )

    def _validate_initialization(self, domain: Domain) -> None:
        for predicate in self.initialization:
            predicate.value._validate(
                predicate.location,
                {},
                self.object_types,
                domain.predicate_definitions,
                domain.type_hierarchy,
                domain.requirements,
            )

    def _validate_goal_condition(self, domain: Domain) -> None:
        self.goal_condition.value._validate(
            self.goal_condition.location,
            {},
            self.object_types,
            domain.predicate_definitions,
            domain.type_hierarchy,
            domain.requirements,
        )

    def _validate(self, domain: Domain) -> None:
        self._validate_used_domain_name(domain)
        self._validate_object_types(domain)
        self._validate_initialization(domain)
        self._validate_goal_condition(domain)
