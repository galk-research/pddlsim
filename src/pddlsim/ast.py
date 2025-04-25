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
from lark.lexer import Token


class Location(ABC):
    @abstractmethod
    def as_str_with_value(self, value: Any) -> str:
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
    def from_token(cls, token: Token) -> "FileLocation":
        if not token.line:
            raise ValueError("token must have line information")

        if not token.column:
            raise ValueError("token must have column information")

        return FileLocation(token.line, token.column)

    def as_str_with_value(self, value: Any) -> str:
        return f"{value} ({self.line}:{self.column})"


@dataclass(frozen=True)
class EmptyLocation(Location):
    def as_str_with_value(self, value: Any) -> str:
        return str(value)


@dataclass(frozen=True, eq=True)
class Locationed(ABC):
    location: Location = field(
        hash=False, compare=False, default_factory=EmptyLocation, kw_only=True
    )

    @abstractmethod
    def as_str_without_location(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.location.as_str_with_value(self.as_str_without_location())


class Requirement(StrEnum):
    STRIPS = ":strips"
    TYPING = ":typing"
    DISJUNCTIVE_PRECONDITIONS = ":disjunctive-preconditions"
    EQUALITY = ":equality"
    PROBABILISTIC_EFFECTS = ":probabilistic-effects"


@dataclass(frozen=True)
class RequirementSet(Locationed):
    requirements: set[Requirement]

    @classmethod
    def from_raw_parts(
        cls,
        requirements: Iterable[Requirement],
        *,
        location: Location | None = None,
    ) -> "RequirementSet":
        requirement_set = set[Requirement]()
        result = RequirementSet(
            requirement_set, location=location if location else EmptyLocation()
        )

        for requirement in requirements:
            if requirement in requirement_set:
                raise ValueError(
                    f"requirement {requirement} used multiple times in {result}"
                )

            requirement_set.add(requirement)

        return result

    def __iter__(self) -> Iterator[Requirement]:
        return iter(self.requirements)

    def __contains__(self, value: Any) -> bool:
        return value in self.requirements

    def as_str_without_location(self) -> str:
        return "requirements section"


@dataclass(frozen=True)
class Identifier(Locationed):
    value: str

    def as_str_without_location(self) -> str:
        return self.value

    @serializer
    def _serialize(self) -> str:
        return self.value

    @classmethod
    def deserialize[I: "Identifier"](cls: type[I], value: str) -> I:
        return cls(value)

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        deserializer(Conversion(cls.deserialize, target=cls))


deserializer(Identifier)


@dataclass(frozen=True)
class Variable(Identifier):
    def as_str(self) -> str:
        return f"?{self.value}"


@dataclass(frozen=True)
class CustomType(Identifier):
    pass


@dataclass(eq=True, frozen=True)
class ObjectType:
    def as_str(self) -> str:
        return "object"


type Type = CustomType | ObjectType


@dataclass(frozen=True)
class Object(Identifier):
    pass


@dataclass(eq=True, frozen=True)
class Typed[T]:
    value: T
    type: Type


@dataclass(frozen=True)
class TypeHierarchy(Locationed):
    _supertypes: Mapping[CustomType, Type]

    @classmethod
    def from_raw_parts(
        cls,
        custom_types: Iterable[Typed[CustomType]],
        *,
        location: Location | None = None,
    ) -> "TypeHierarchy":
        supertypes = {}

        for custom_type in custom_types:
            if custom_type.value in supertypes:
                raise ValueError(
                    f"type '{custom_type.value}' is defined multiple times"
                )

            supertypes[custom_type.value] = custom_type.type

        return TypeHierarchy(
            supertypes, location=location if location else EmptyLocation()
        )

    def __iter__(self) -> Iterator[Typed[CustomType]]:
        return (
            Typed(subtype, supertype)
            for subtype, supertype in self._supertypes.items()
        )

    def supertype(self, custom_type: CustomType) -> Type:
        return self._supertypes[custom_type]

    def is_compatible(self, test_type: Type, tester_type: Type) -> bool:
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

    def as_str_without_location(self) -> str:
        return "types section"


@dataclass(frozen=True)
class PredicateDefinition:
    name: Identifier
    parameters: list[Typed[Variable]]

    @classmethod
    def from_raw_parts(
        cls,
        name: Identifier,
        parameters: list[Typed[Variable]],
    ) -> "PredicateDefinition":
        variables = set()

        for parameter in parameters:
            if parameter.value in variables:
                raise ValueError(
                    f"parameter '{parameter.value}' of predicate definition '{name}' defined multiple times"  # noqa: E501
                )

            variables.add(parameter.value)

        return PredicateDefinition(name, parameters)

    def _validate(self, type_hierarchy: TypeHierarchy) -> None:
        for parameter in self.parameters:
            if (
                isinstance(parameter.type, CustomType)
                and parameter.type not in type_hierarchy
            ):
                raise ValueError(
                    f"parameter '{parameter.value}' of predicate definition '{self.name}' uses an undefined type: '{parameter.type}'"  # noqa: E501
                )


type Argument = Variable | Object


@dataclass(frozen=True)
class AndCondition[A: Argument]:
    subconditions: list["Condition[A]"]

    def _validate(
        self,
        variable_types: Mapping[Variable, Type],
        object_types: Mapping[Object, Type],
        predicate_definitions: Mapping[Identifier, PredicateDefinition],
        type_hierarchy: TypeHierarchy,
        requirements: RequirementSet,
    ) -> None:
        for subcondition in self.subconditions:
            subcondition._validate(
                variable_types,
                object_types,
                predicate_definitions,
                type_hierarchy,
                requirements,
            )


@dataclass(frozen=True)
class OrCondition[A: Argument](Locationed):
    subconditions: list["Condition[A]"]

    def _validate(
        self,
        variable_types: Mapping[Variable, Type],
        object_types: Mapping[Object, Type],
        predicate_definitions: Mapping[Identifier, PredicateDefinition],
        type_hierarchy: TypeHierarchy,
        requirements: RequirementSet,
    ) -> None:
        if Requirement.DISJUNCTIVE_PRECONDITIONS not in requirements:
            raise ValueError(
                f"{self} used in condition, but '{Requirement.DISJUNCTIVE_PRECONDITIONS}' is not used"  # noqa: E501
            )

        for subcondition in self.subconditions:
            subcondition._validate(
                variable_types,
                object_types,
                predicate_definitions,
                type_hierarchy,
                requirements,
            )

    def as_str_without_location(self) -> str:
        return "disjunction"


@dataclass(frozen=True)
class NotCondition[A: Argument]:
    base_condition: "Condition[A]"

    def _validate(
        self,
        variable_types: Mapping[Variable, Type],
        object_types: Mapping[Object, Type],
        predicate_definitions: Mapping[Identifier, PredicateDefinition],
        type_hierarchy: TypeHierarchy,
        requirements: RequirementSet,
    ) -> None:
        self.base_condition._validate(
            variable_types,
            object_types,
            predicate_definitions,
            type_hierarchy,
            requirements,
        )


@dataclass(frozen=True)
class EqualityCondition[A: Argument](Locationed):
    left_side: A
    right_side: A

    def _validate(
        self,
        variable_types: Mapping[Variable, Type],
        object_types: Mapping[Object, Type],
        _predicate_definitions: Mapping[Identifier, PredicateDefinition],
        _type_hierarchy: TypeHierarchy,
        requirements: RequirementSet,
    ) -> None:
        if Requirement.EQUALITY not in requirements:
            raise ValueError(
                f"{self} used in condition, but '{Requirement.EQUALITY}' is not used"  # noqa: E501
            )

        def validate_argument(argument: A) -> None:
            match argument:
                case Variable():
                    if argument not in variable_types:
                        raise ValueError(f"variable '{argument}' is undefined")
                case Object():
                    if argument not in object_types:
                        raise ValueError(f"constant '{argument}' is undefined")

        validate_argument(self.left_side)
        validate_argument(self.right_side)

    def as_str_without_location(self) -> str:
        return "equality predicate"


@dataclass(frozen=True)
class Predicate[A: Argument]:
    name: Identifier
    assignment: tuple[A, ...]

    def _validate(
        self,
        variable_types: Mapping[Variable, Type],
        object_types: Mapping[Object, Type],
        predicate_definitions: Mapping[Identifier, PredicateDefinition],
        type_hierarchy: TypeHierarchy,
        _requirements: RequirementSet,
    ) -> None:
        if self.name not in predicate_definitions:
            raise ValueError(f"predicate {self.name} is undefined")

        predicate_definition = predicate_definitions[self.name]

        for parameter, argument in zip(
            predicate_definition.parameters, self.assignment, strict=True
        ):
            match argument:
                case Variable():
                    if argument not in variable_types:
                        raise ValueError(f"variable '{argument}' is undefined")

                    argument_type = variable_types[argument]  # type: ignore
                case Object():
                    if argument not in object_types:
                        raise ValueError(f"constant '{argument}' is undefined")

                    argument_type = object_types[argument]  # type: ignore

            if not type_hierarchy.is_compatible(argument_type, parameter.type):
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
    base_predicate: Predicate[A]

    def _validate(
        self,
        variable_types: Mapping[Variable, Type],
        object_types: Mapping[Object, Type],
        predicate_definitions: Mapping[Identifier, PredicateDefinition],
        type_hierarchy: TypeHierarchy,
        requirements: RequirementSet,
    ) -> None:
        self.base_predicate._validate(
            variable_types,
            object_types,
            predicate_definitions,
            type_hierarchy,
            requirements,
        )


type Atom[A: Argument] = Predicate[A] | NotPredicate[A]


@dataclass(frozen=True)
class AndEffect[A: Argument]:
    subeffects: list["Effect[A]"]

    def _validate(
        self,
        variable_types: Mapping[Variable, Type],
        object_types: Mapping[Object, Type],
        predicate_definitions: Mapping[Identifier, PredicateDefinition],
        type_hierarchy: TypeHierarchy,
        requirements: RequirementSet,
    ) -> None:
        for subeffect in self.subeffects:
            subeffect._validate(
                variable_types,
                object_types,
                predicate_definitions,
                type_hierarchy,
                requirements,
            )


@dataclass(frozen=True)
class ProbabilisticEffect[A: Argument](Locationed):
    _possible_effects: list["Effect[A]"]
    _cummulative_probabilities: list[Decimal]

    @classmethod
    def from_possibilities(
        cls,
        possibilities: list[tuple[Decimal, "Effect[A]"]],
        *,
        location: Location | None = None,
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

        return ProbabilisticEffect(
            possible_effects,
            cummulative_probabilities,
            location=location if location else EmptyLocation(),
        )

    def choose_possibility(self, rng: Random) -> "Effect[A]":
        index = bisect.bisect(self._cummulative_probabilities, rng.random())

        if index == len(self._possible_effects):
            return AndEffect([])  # Empty effect

        return self._possible_effects[index]

    def _validate(
        self,
        variable_types: Mapping[Variable, Type],
        object_types: Mapping[Object, Type],
        predicate_definitions: Mapping[Identifier, PredicateDefinition],
        type_hierarchy: TypeHierarchy,
        requirements: RequirementSet,
    ) -> None:
        if Requirement.PROBABILISTIC_EFFECTS not in requirements:
            raise ValueError(
                f"{self} used in action, but '{Requirement.PROBABILISTIC_EFFECTS}' is not used"  # noqa: E501
            )

        for effect in self._possible_effects:
            effect._validate(
                variable_types,
                object_types,
                predicate_definitions,
                type_hierarchy,
                requirements,
            )

    def as_str_without_location(self) -> str:
        return "probabilistic effect"


type Effect[A: Argument] = AndEffect[A] | ProbabilisticEffect[A] | Atom[A]


@dataclass(frozen=True)
class ActionDefinition:
    name: Identifier
    variable_types: dict[Variable, Type]
    precondition: Condition[Argument]
    effect: Effect[Argument]

    @classmethod
    def from_raw_parts(
        cls,
        name: Identifier,
        parameters: list[Typed[Variable]],
        precondition: Condition[Argument],
        effect: Effect[Argument],
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
        constant_types: Mapping[Object, Type],
        predicate_definitions: Mapping[Identifier, PredicateDefinition],
        type_hierarchy: TypeHierarchy,
        requirements: RequirementSet,
    ) -> None:
        # The dictionary is insertion ordered, so this is fine
        for variable, type in self.variable_types.items():
            if isinstance(type, CustomType) and type not in type_hierarchy:
                raise ValueError(
                    f"parameter '{variable}' of action definition '{self.name}' uses an undefined type: '{type}'"  # noqa: E501
                )

        self.precondition._validate(
            self.variable_types,
            constant_types,
            predicate_definitions,
            type_hierarchy,
            requirements,
        )
        self.effect._validate(
            self.variable_types,
            constant_types,
            predicate_definitions,
            type_hierarchy,
            requirements,
        )


@dataclass(frozen=True)
class Domain:
    name: Identifier
    requirements: RequirementSet
    type_hierarchy: TypeHierarchy = field(init=False)
    _type_hierarchy: InitVar[TypeHierarchy | None]
    constant_types: Mapping[Object, Type]
    predicate_definitions: Mapping[Identifier, PredicateDefinition]
    action_definitions: Mapping[Identifier, ActionDefinition]

    @classmethod
    def from_raw_parts(
        cls,
        name: Identifier,
        requirements: RequirementSet,
        type_hierarchy: TypeHierarchy | None,
        constants: Iterable[Typed[Object]],
        predicate_definitions: Iterable[PredicateDefinition],
        action_definitions: Iterable[ActionDefinition],
    ) -> "Domain":
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
            requirements,
            type_hierarchy,
            constant_types,
            predicate_definition_map,
            action_definition_map,
        )

    def __post_init__(self, type_hierarchy: TypeHierarchy | None) -> None:
        object.__setattr__(
            self,
            "type_hierarchy",
            type_hierarchy if type_hierarchy else TypeHierarchy({}),
        )
        self._validate(type_hierarchy)

    def _validate_type_hierarchy(
        self, type_hierarchy: TypeHierarchy | None
    ) -> None:
        if (
            Requirement.TYPING not in self.requirements
            and type_hierarchy is not None
        ):
            raise ValueError(
                f"{type_hierarchy} is defined in domain, but '{Requirement.TYPING}' requirement is not used"  # noqa: E501
            )

    def _validate_constant_types(self) -> None:
        for constant, type in self.constant_types.items():
            if isinstance(type, CustomType) and type not in self.type_hierarchy:
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

    def _validate(self, type_hierarchy: TypeHierarchy | None) -> None:
        self._validate_type_hierarchy(type_hierarchy)
        self._validate_constant_types()
        self._validate_predicate_definitions()
        self._validate_action_definitions()


@dataclass(frozen=True)
class RawProblemParts:
    name: Identifier
    used_domain_name: Identifier
    objects: list[Typed[Object]]
    initialization: list[Predicate[Object]]
    goal_condition: Condition[Object]


@dataclass(frozen=True)
class Problem:
    name: Identifier
    used_domain_name: Identifier
    object_types: Mapping[Object, Type]
    initialization: Set[Predicate[Object]]
    goal_condition: Condition[Object]
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
            if type not in domain.type_hierarchy:
                raise ValueError(
                    f"object '{object_}' is of non-existent type: '{type}'"
                )

    def _validate_initialization(self, domain: Domain) -> None:
        for predicate in self.initialization:
            predicate._validate(
                {},
                self.object_types,
                domain.predicate_definitions,
                domain.type_hierarchy,
                domain.requirements,
            )

    def _validate_goal_condition(self, domain: Domain) -> None:
        self.goal_condition._validate(
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
