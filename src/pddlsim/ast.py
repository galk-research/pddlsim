"""Definitions for the AST PDDLSIM uses for representing PDDL definitions."""

import bisect
import itertools
import operator
import re
from abc import ABC, abstractmethod
from collections import ChainMap
from collections.abc import (
    Container,
    Iterable,
    Iterator,
    Mapping,
    Set,
    Sized,
)
from dataclasses import InitVar, dataclass, field
from decimal import Decimal
from enum import StrEnum
from random import Random
from typing import Any, ClassVar, TypedDict, override

from koda_validate import (
    StringValidator,
    TypedDictValidator,
    Validator,
)
from lark.lexer import Token

from pddlsim._serde import Serdeable


class Location(ABC):
    """A location of an AST item."""

    @abstractmethod
    def as_str_with_value(self, value: Any) -> str:
        """Display the value with this location as an annotation."""
        raise NotImplementedError


@dataclass(frozen=True)
class FileLocation(Location):
    """A location of an AST item in a file."""

    line: int
    """The line in which the AST item started."""
    column: int
    """The column in which the AST item started."""

    def __post_init__(self) -> None:
        """Verify the line and column numbers are positive."""
        if self.line <= 0:
            raise ValueError(
                f"line number must be positive, is instead {self.line}"
            )

        if self.column <= 0:
            raise ValueError(
                f"column number must be positive, is instead {self.column}"
            )

    @classmethod
    def _from_token(cls, token: Token) -> "FileLocation":
        if not token.line:
            raise ValueError("token must have line information")

        if not token.column:
            raise ValueError("token must have column information")

        return FileLocation(token.line, token.column)

    @override
    def as_str_with_value(self, value: Any) -> str:
        return f"`{value}` ({self.line}:{self.column})"


@dataclass(frozen=True)
class EmptyLocation(Location):
    """A dummy location for an AST item.

    Useful for assigning locations to AST items generated programmatically.
    """

    @override
    def as_str_with_value(self, value: Any) -> str:
        return str(value)


@dataclass(frozen=True, eq=True)
class Locationed(ABC):
    """Base class for an AST item with a location attached."""

    location: Location = field(
        hash=False,
        compare=False,
        default_factory=EmptyLocation,
        kw_only=True,
    )
    """The location of the AST item."""

    @abstractmethod
    def _as_str_without_location(self) -> str:
        """Return a string of the AST item, without location information."""
        raise NotImplementedError

    @override
    def __str__(self) -> str:
        return self.location.as_str_with_value(self._as_str_without_location())


class Requirement(StrEnum):
    """Represents a PDDL requirement (with extensions)."""

    STRIPS = ":strips"
    """Doesn't add any new features and is assumed."""
    TYPING = ":typing"
    """Allows to specify types for objects, and impose types on variables."""
    DISJUNCTIVE_PRECONDITIONS = ":disjunctive-preconditions"
    """Allows usage of `or` in conditions."""
    NEGATIVE_PRECONDITIONS = ":negative-preconditions"
    """Allows usage of `not` in conditions."""
    EQUALITY = ":equality"
    """Allows usage of `=` predicates."""
    PROBABILISTIC_EFFECTS = ":probabilistic-effects"
    """Allows usage of probabilistic effects."""

    FALLIBLE_ACTIONS = ":fallible-actions"
    """Allows specifying [action fallibilities](https://github.com/galk-research/pddlsim/wiki/Fallible-Actions)."""
    REVEALABLES = ":revealables"
    """Allows problems to use [revealables](https://github.com/galk-research/pddlsim/wiki/Revealables)."""
    MULTIPLE_GOALS = ":multiple-goals"
    """Allows problems specify [multiple goals](https://github.com/galk-research/pddlsim/wiki/Multiple-Goals)."""

    @override
    def __repr__(self) -> str:
        return self.value


@dataclass(frozen=True)
class RequirementSet(Iterable, Container, Locationed):
    """Represents a set of requirements, specified for domains and problems."""

    requirements: set[Requirement]

    @classmethod
    def from_raw_parts(
        cls,
        requirements: Iterable[Requirement],
        *,
        location: Location | None = None,
    ) -> "RequirementSet":
        """Construct a `RequirementSet` from subnodes received from a parser."""
        requirement_set = set[Requirement]()
        result = RequirementSet(
            requirement_set, location=location if location else EmptyLocation()
        )

        for requirement in requirements:
            if requirement in requirement_set:
                raise ValueError(
                    f"requirement {requirement} appears multiple times in {result}"  # noqa: E501
                )

            requirement_set.add(requirement)

        return result

    @override
    def __iter__(self) -> Iterator[Requirement]:
        return iter(self.requirements)

    @override
    def __contains__(self, value: Any) -> bool:
        return value in self.requirements

    @override
    def _as_str_without_location(self) -> str:
        return "requirements section"

    @override
    def __repr__(self) -> str:
        return f"(:requirements {' '.join(map(repr, self.requirements))})"


@dataclass(frozen=True, eq=True)
class Identifier(Locationed, Serdeable[str]):
    """Represents a PDDL identifier."""

    value: str
    """The identifier's text."""

    _IDENTIFIER_REGEX: ClassVar = re.compile(r"[a-zA-Z][a-zA-Z0-9\-_]*")

    def __post_init__(self) -> None:
        """Validate the identifier (e.g., check if starts with letter)."""
        if not self._IDENTIFIER_REGEX.match(self.value):
            raise ValueError(f"{self.value} is not a valid identifier")

    @override
    def serialize(self) -> str:
        return self.value

    @classmethod
    @override
    def _validator(cls) -> Validator[str]:
        return StringValidator()

    @classmethod
    @override
    def _create(cls, value: str) -> "Identifier":
        return cls(value)

    @override
    def _as_str_without_location(self) -> str:
        return self.value

    @override
    def __repr__(self) -> str:
        return self._as_str_without_location()


@dataclass(frozen=True, eq=True)
class Variable(Identifier):
    """Represents a PDDL variable."""

    @override
    def _as_str_without_location(self) -> str:
        return f"?{self.value}"

    @override
    def __repr__(self) -> str:
        return self._as_str_without_location()


@dataclass(frozen=True, eq=True)
class CustomType(Identifier):
    """Represents a user-defineable type in PDDL."""

    @override
    def __repr__(self) -> str:
        return self._as_str_without_location()


@dataclass(eq=True, frozen=True)
class ObjectType:
    """Represents the type `object` in PDDL. All types are subtypes of it."""

    @override
    def __repr__(self) -> str:
        return "object"


type Type = CustomType | ObjectType
"""Represents the type of a PDDL object/variable."""


@dataclass(frozen=True, eq=True)
class Object(Identifier):
    """Represents the name of an object in PDDL."""

    @override
    def __repr__(self) -> str:
        return self._as_str_without_location()


@dataclass(eq=True, frozen=True)
class Typed[T]:
    """Represents an AST item with a type attached."""

    value: T
    """The AST item."""
    type: Type
    """The attached type."""

    @override
    def __repr__(self) -> str:
        return f"{self.value!r} - {self.type!r}"


def _as_typed_iter[T](mapping: Mapping[T, Type]) -> Iterator[Typed[T]]:
    return (Typed(value, type) for value, type in mapping.items())


@dataclass(frozen=True)
class TypeHierarchy(Iterable, Container, Locationed):
    """Represents the `:types` section in PDDL."""

    _supertypes: Mapping[CustomType, Type] = field(default_factory=dict)

    @classmethod
    def from_raw_parts(
        cls,
        custom_types: Iterable[Typed[CustomType]],
        *,
        location: Location | None = None,
    ) -> "TypeHierarchy":
        """Construct a `TypeHierarchy` from subnodes received from a parser."""
        supertypes: dict[CustomType, Type] = {}
        result = TypeHierarchy(
            supertypes, location=location if location else EmptyLocation()
        )

        for custom_type in custom_types:
            if custom_type.value in supertypes:
                raise ValueError(
                    f"type {custom_type.value} is defined multiple times in {result}"  # noqa: E501
                )

            supertypes[custom_type.value] = custom_type.type

        return result

    @override
    def __iter__(self) -> Iterator[Typed[CustomType]]:
        return _as_typed_iter(self._supertypes)

    def supertype(self, custom_type: CustomType) -> Type:
        """Return the immediate supertype of the provided type.

        The passed value is a `CustomType`, as `ObjectType` has no supertype.
        """
        return self._supertypes[custom_type]

    def is_compatible(self, test_type: Type, tester_type: Type) -> bool:
        """Check if `test_type` is a subtype of `tester_type`.

        This check returns `True` for equal types, and so isn't
        a strict subtyping check.
        """
        if test_type == tester_type:
            return True
        elif isinstance(test_type, CustomType):
            return self.is_compatible(self.supertype(test_type), tester_type)
        else:
            return False

    @override
    def __contains__(self, item: Any) -> bool:
        return item in self._supertypes

    @override
    def _as_str_without_location(self) -> str:
        return "types section"

    @override
    def __repr__(self) -> str:
        return f"(:types {' '.join(map(repr, self))})"


@dataclass(frozen=True)
class PredicateDefinition:
    """Represents a predicate definition (in domain's `:predicates` section)."""

    name: Identifier
    parameters: list[Typed[Variable]]

    @classmethod
    def from_raw_parts(
        cls,
        name: Identifier,
        parameters: list[Typed[Variable]],
    ) -> "PredicateDefinition":
        """Construct a `PredicateDefinition` from subnodes returned by a parser."""  # noqa: E501
        variables = set()

        for parameter in parameters:
            if parameter.value in variables:
                raise ValueError(
                    f"parameter {parameter.value} defined multiple times in predicate definition {name}"  # noqa: E501
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
                    f"parameter {parameter.value} of predicate definition {self.name} is of undefined type {parameter.type}"  # noqa: E501
                )

    @override
    def __repr__(self) -> str:
        return f"({self.name!r} {' '.join(map(repr, self.parameters))})"


type Argument = Variable | Object


@dataclass(frozen=True)
class AndCondition[A: Argument]:
    """Represents a conjunction (`and`) of PDDL conditions."""

    subconditions: list["Condition[A]"]
    """The subconditions being conjuncted."""

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

    @override
    def __repr__(self) -> str:
        return f"(and {' '.join(map(repr, self.subconditions))})"


@dataclass(frozen=True)
class OrCondition[A: Argument](Locationed):
    """Represents a disjunction (`or`) of PDDL conditions."""

    subconditions: list["Condition[A]"]
    """The subconditions being disjuncted."""

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
                f"{self} used in condition, but `{Requirement.DISJUNCTIVE_PRECONDITIONS}` is not in {requirements}"  # noqa: E501
            )

        for subcondition in self.subconditions:
            subcondition._validate(
                variable_types,
                object_types,
                predicate_definitions,
                type_hierarchy,
                requirements,
            )

    @override
    def _as_str_without_location(self) -> str:
        return "disjunction"

    @override
    def __repr__(self) -> str:
        return f"(or {' '.join(map(repr, self.subconditions))})"


@dataclass(frozen=True)
class NotCondition[A: Argument](Locationed):
    """Represents the negation (`not`) of a PDDL condition."""

    base_condition: "Condition[A]"
    """The base condition being negated."""

    def _validate(
        self,
        variable_types: Mapping[Variable, Type],
        object_types: Mapping[Object, Type],
        predicate_definitions: Mapping[Identifier, PredicateDefinition],
        type_hierarchy: TypeHierarchy,
        requirements: RequirementSet,
    ) -> None:
        if Requirement.NEGATIVE_PRECONDITIONS not in requirements:
            raise ValueError(
                f"{self} used in condition, but `{Requirement.NEGATIVE_PRECONDITIONS}` is not in {requirements}"  # noqa: E501
            )

        self.base_condition._validate(
            variable_types,
            object_types,
            predicate_definitions,
            type_hierarchy,
            requirements,
        )

    @override
    def _as_str_without_location(self) -> str:
        return "negation"

    @override
    def __repr__(self) -> str:
        return f"(not {self.base_condition!r})"


@dataclass(frozen=True)
class EqualityCondition[A: Argument](Locationed):
    """Represents an equality predicate (`=`) in PDDL."""

    left_side: A
    """Left side of the equality."""
    right_side: A
    """Right side of the equality."""

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
                f"{self} used in condition, but `{Requirement.EQUALITY}` is not in {requirements}"  # noqa: E501
            )

        def validate_argument(argument: A) -> None:
            match argument:
                case Variable():
                    if argument not in variable_types:
                        raise ValueError(
                            f"variable {argument} in {self} is undefined"
                        )
                case Object():
                    if argument not in object_types:
                        raise ValueError(
                            f"object {argument} in {self} is undefined"
                        )

        validate_argument(self.left_side)
        validate_argument(self.right_side)

    @override
    def _as_str_without_location(self) -> str:
        return "equality predicate"

    @override
    def __repr__(self) -> str:
        return f"(= {self.left_side!r} {self.right_side!r})"


class _SerializedPredicate(TypedDict):
    name: Any
    assignment: list[Any]


@dataclass(frozen=True)
class Predicate[A: Argument](Serdeable[_SerializedPredicate]):
    """Represents the instantiation of a predicate in PDDL."""

    name: Identifier
    """The name of the predicate being instantiated."""
    assignment: tuple[A, ...]
    """The instantiation of the predicate."""

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
                        raise ValueError(
                            f"variable {argument} in {self.name} is undefined"
                        )

                    argument_type = variable_types[argument]  # type: ignore
                case Object():
                    if argument not in object_types:
                        raise ValueError(
                            f"object {argument} in {self.name} is undefined"
                        )

                    argument_type = object_types[argument]  # type: ignore

            if not type_hierarchy.is_compatible(argument_type, parameter.type):
                raise ValueError(
                    f"argument {argument} in {self.name} is of type {argument_type}, but is supposed to be of type {parameter.type}"  # noqa: E501
                )

    @override
    def serialize(self) -> _SerializedPredicate:
        return _SerializedPredicate(
            name=self.name.serialize(),
            assignment=[argument.serialize() for argument in self.assignment],
        )

    @classmethod
    @override
    def _validator(cls) -> Validator[_SerializedPredicate]:
        return TypedDictValidator(_SerializedPredicate)

    @classmethod
    @override
    def _create(cls, value: _SerializedPredicate) -> "Predicate[A]":
        return Predicate(
            Identifier.deserialize(value["name"]),
            tuple(
                Object.deserialize(argument)  # type: ignore
                for argument in value["assignment"]
            ),
        )

    @override
    def __repr__(self) -> str:
        return f"({self.name!r} {' '.join(map(repr, self.assignment))})"


type Condition[A: Argument] = (
    AndCondition[A]
    | OrCondition[A]
    | NotCondition[A]
    | EqualityCondition[A]
    | Predicate[A]
)
"""Represents a condition in PDDL, over objects, or variables."""


@dataclass(frozen=True)
class NotPredicate[A: Argument]:
    """Represents the effect of removing a predicate from the state in PDDL."""

    base_predicate: Predicate[A]
    """The predicate to remove."""

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

    @override
    def __repr__(self) -> str:
        return f"(not {self.base_predicate!r})"


type Atom[A: Argument] = Predicate[A] | NotPredicate[A]
"""Represents an effect adding/removing a predicate from the state in PDDL."""


@dataclass(frozen=True)
class AndEffect[A: Argument]:
    """Represents an effect of applying all subeffects to the state in PDDL."""

    subeffects: list["Effect[A]"] = field(default_factory=list)
    """The subeffects to apply to the state."""

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

    @override
    def __repr__(self) -> str:
        return f"(and {' '.join(map(repr, self.subeffects))})"


@dataclass(frozen=True)
class ProbabilisticEffect[A: Argument](Iterable, Locationed):
    """Represents a probabilistic effect, choosing a subeffect at random.

    The primary constructor for this class is
    `ProbabilisticEffect.from_possibilities`.
    """

    _possible_effects: list["Effect[A]"]
    _cummulative_probabilities: list[Decimal]

    @classmethod
    def from_possibilities(
        cls,
        possibilities: list[tuple[Decimal, "Effect[A]"]],
        *,
        location: Location | None = None,
    ) -> "ProbabilisticEffect":
        """Construct a `ProbabilisticEffect` from effect-probability pairs."""
        possible_effects: list[Effect[A]] = []
        cummulative_probabilities: list[Decimal] = []
        cummulative_probability = Decimal()

        result = ProbabilisticEffect(
            possible_effects,
            cummulative_probabilities,
            location=location if location else EmptyLocation(),
        )

        for probability, possibility in possibilities:
            if probability < 0:
                raise ValueError(
                    f"probability {probability} in {result} is negative"
                )

            cummulative_probability += probability

            cummulative_probabilities.append(cummulative_probability)
            possible_effects.append(possibility)

        cummulative_probabilities = list(
            itertools.accumulate(
                (probability for probability, _ in possibilities), operator.add
            )
        )

        if cummulative_probability > 1:
            raise ValueError(
                f"total probability of {result} mustn't be greater than 1, is {cummulative_probability}"  # noqa: E501
            )

        return result

    def choose_possibility(self, rng: Random | None = None) -> "Effect[A]":
        """Choose an effect according to their probabilities.

        Optionally, one can specify the RNG to use for the calculations.
        """
        index = bisect.bisect(
            self._cummulative_probabilities, (rng if rng else Random()).random()
        )

        if index == len(self._possible_effects):
            return AndEffect()  # Empty effect

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
                f"{self} used in action, but `{Requirement.PROBABILISTIC_EFFECTS}` does not appear in {requirements}"  # noqa: E501
            )

        for effect in self._possible_effects:
            effect._validate(
                variable_types,
                object_types,
                predicate_definitions,
                type_hierarchy,
                requirements,
            )

    @override
    def _as_str_without_location(self) -> str:
        return "probabilistic effect"

    @override
    def __iter__(self) -> Iterator[tuple[Decimal, "Effect[A]"]]:
        probabilities = itertools.chain(
            (self._cummulative_probabilities[0],),
            (
                b - a
                for a, b in itertools.pairwise(self._cummulative_probabilities)
            ),
        )

        return zip(probabilities, self._possible_effects, strict=True)

    @override
    def __repr__(self) -> str:
        def repr_subeffect(
            pair: tuple[Decimal, "Effect[A]"],
        ) -> str:
            return f"{pair[0]} {pair[1]!r}"

        return f"(probabilistic {' '.join(map(repr_subeffect, self))})"


type Effect[A: Argument] = AndEffect[A] | ProbabilisticEffect[A] | Atom[A]
"""Represents a PDDL effect, over objects, or variables."""


@dataclass(frozen=True)
class ActionDefinition:
    """Represents an action definition in PDDL."""

    name: Identifier
    """The name of the action."""
    variable_types: dict[Variable, Type]
    """The type of each parameter."""
    precondition: Condition[Argument]
    """The precondition of the action."""
    effect: Effect[Argument]
    """The effect of the action."""

    @classmethod
    def from_raw_parts(
        cls,
        name: Identifier,
        parameters: list[Typed[Variable]],
        precondition: Condition[Argument],
        effect: Effect[Argument],
    ) -> "ActionDefinition":
        """Construct an `ActionDefinition` from subnodes returned from a parser."""  # noqa: E501
        variable_types = {}

        for parameter in parameters:
            if parameter.value in variable_types:
                raise ValueError(
                    f"parameter with name {parameter.value} is defined in action definition {name} multiple times"  # noqa: E501
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
                    f"parameter {variable} of action definition {self.name} is of an undefined type {type}"  # noqa: E501
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

    @override
    def __repr__(self) -> str:
        parameters = _as_typed_iter(self.variable_types)
        parameters_section = f":parameters ({' '.join(map(repr, parameters))})"

        return f"(:action {self.name!r} {parameters_section} :precondition {self.precondition!r} :effect {self.effect!r})"  # noqa: E501


@dataclass(frozen=True)
class Domain:
    """Represents a PDDL domain."""

    name: Identifier
    """The name of the domain."""
    requirements: RequirementSet
    """The domain's requirements"""
    type_hierarchy: TypeHierarchy
    """The domain's type hierarchy."""
    constant_types: dict[Object, Type]
    """The domain's constants, and their types."""
    predicate_definitions: Mapping[Identifier, PredicateDefinition]
    """The domain's predicate definitions."""
    action_definitions: Mapping[Identifier, ActionDefinition]
    """The domain's action definitions."""

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
        """Construct a `Domain` from the subnodes returned by a parser."""
        if (
            Requirement.TYPING not in requirements
            and type_hierarchy is not None
        ):
            raise ValueError(
                f"{type_hierarchy} is defined in domain, but `{Requirement.TYPING}` does not appear in {requirements}"  # noqa: E501
            )

        constant_types = {}

        for constant in constants:
            if constant.value in constant_types:
                raise ValueError(
                    f"constant with name {constant.value} is defined multiple times"  # noqa: E501
                )

            constant_types[constant.value] = constant.type

        predicate_definition_map = {}

        for predicate_definition in predicate_definitions:
            if predicate_definition.name in predicate_definition_map:
                raise ValueError(
                    f"predicate with name {predicate_definition.name} is defined multiple times"  # noqa: E501
                )

            predicate_definition_map[predicate_definition.name] = (
                predicate_definition
            )

        action_definition_map = {}

        for action_definition in action_definitions:
            if action_definition.name in action_definition_map:
                raise ValueError(
                    f"action with name {action_definition.name} is defined multiple times"  # noqa: E501
                )

            action_definition_map[action_definition.name] = action_definition
        return Domain(
            name,
            requirements,
            type_hierarchy if type_hierarchy else TypeHierarchy(),
            constant_types,
            predicate_definition_map,
            action_definition_map,
        )

    def __post_init__(self) -> None:
        """Validate the domain (e.g., make sure all referenced types exist)."""
        self._validate()

    def _validate_constant_types(self) -> None:
        for constant, type in self.constant_types.items():
            if isinstance(type, CustomType) and type not in self.type_hierarchy:
                raise ValueError(
                    f"constant {constant} is of undefined type {type}"
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

    def _validate(self) -> None:
        self._validate_constant_types()
        self._validate_predicate_definitions()
        self._validate_action_definitions()

    @override
    def __repr__(self) -> str:
        domain_name = f"(domain {self.name!r})"

        constants_section = f"(:constants {' '.join(map(repr, _as_typed_iter(self.constant_types)))})"  # noqa: E501

        predicate_definition_reprs = map(
            repr, self.predicate_definitions.values()
        )
        predicates_setion = (
            f"(:predicates {' '.join(predicate_definition_reprs)})"
        )

        action_definitions = " ".join(
            map(repr, self.action_definitions.values())
        )

        return f"(define {domain_name} {self.requirements!r} {self.type_hierarchy!r} {constants_section} {predicates_setion} {action_definitions})"  # noqa: E501


@dataclass(frozen=True, eq=True)
class ActionFallibility:
    """Represents an [action fallibility](https://github.com/galk-research/pddlsim/wiki/Fallible-Actions)."""

    name: Identifier
    """The name of the action."""
    condition: Condition[Object]
    """The failure condition of the action."""
    with_probability: Decimal = field(
        default=Decimal("1"), compare=False, hash=False
    )
    """The probability of failure on condition satisfaction."""

    def __post_init__(self) -> None:
        """Make sure the specified probability is a valid probability."""
        if not (0 <= self.with_probability <= 1):
            raise ValueError(
                f"fallible action {self.name} is with impossible probability {self.with_probability}"  # noqa: E501
            )


@dataclass(frozen=True)
class ActionFallibilitySet(Iterable, Locationed):
    """Represents the `:fails` section of a PDDL problem."""

    _fallible_actions: Set[ActionFallibility] = field(default_factory=set)

    @classmethod
    def from_raw_parts(
        cls,
        fallibilities: Iterable[ActionFallibility],
        *,
        location: Location | None = None,
    ) -> "ActionFallibilitySet":
        """Construct an `ActionFallibilitySet` from the subnodes returned by a parser."""  # noqa: E501
        action_fallibilities_set = set()

        for action_fallibility in fallibilities:
            if action_fallibility in action_fallibilities_set:
                raise ValueError(
                    f"{action_fallibility} is defined multiple times"
                )

            action_fallibilities_set.add(action_fallibility)

        return ActionFallibilitySet(
            action_fallibilities_set,
            location=location if location else EmptyLocation(),
        )

    @override
    def _as_str_without_location(self) -> str:
        return "action fallibilities section"

    @override
    def __iter__(self) -> Iterator[ActionFallibility]:
        return iter(self._fallible_actions)


@dataclass(frozen=True, eq=True)
class Revealable:
    """Represents a [revealable](https://github.com/galk-research/pddlsim/wiki/Revealables)."""

    effect: Effect[Object]
    """The revealable's effect."""
    condition: Condition[Object]
    """The revealable's activation condition."""
    with_probability: Decimal = field(
        default=Decimal("1"), compare=False, hash=False
    )
    """The revealable's activation probability."""

    def __post_init__(self) -> None:
        """Make sure the probability specified is between 0 and 1."""
        if not (0 <= self.with_probability <= 1):
            raise ValueError(
                f"{self} is with impossible probability {self.with_probability}"
            )


@dataclass(frozen=True)
class RevealableSet(Iterable, Locationed):
    """Represents the `:reveals` section of a PDDL problem."""

    _revealables: Set[Revealable] = field(default_factory=set)

    @classmethod
    def from_raw_parts(
        cls,
        revealables: Iterable[Revealable],
        *,
        location: Location | None = None,
    ) -> "RevealableSet":
        """Construct a `RevealableSet` from the subnodes returned by a parser."""  # noqa: E501
        revealable_set = set()

        for revealable in revealables:
            if revealable in revealable_set:
                raise ValueError(f"{revealable} is defined multiple times")

            revealable_set.add(revealable)

        return RevealableSet(
            revealable_set,
            location=location if location else EmptyLocation(),
        )

    @override
    def _as_str_without_location(self) -> str:
        return "revealables section"

    @override
    def __iter__(self) -> Iterator[Revealable]:
        return iter(self._revealables)


@dataclass(frozen=True)
class GoalList(Iterable, Sized, Locationed):
    """Represents the `:goals`/`:goal` section of the PDDL problem."""

    _goals: list[Condition[Object]] = field(default_factory=list)

    def _as_str_without_location(self) -> str:
        return "goal conditions"

    @override
    def __iter__(self) -> Iterator[Condition[Object]]:
        return iter(self._goals)

    def get_goal(self, goal_index: int) -> Condition[Object]:
        """Return the goal associated with the index."""
        return self._goals[goal_index]

    @override
    def __len__(self) -> int:
        return len(self._goals)


@dataclass(frozen=True)
class RawProblem:
    """Represents a PDDL problem, without any validation."""

    name: Identifier
    """The problem's name."""
    used_domain_name: Identifier
    """The name of the domain used by the problem."""
    requirements: RequirementSet
    """The problem's requirements."""
    object_types: dict[Object, Type]
    """The objects of the PDDL problem (and their types)."""
    action_fallibilities: ActionFallibilitySet
    """The action fallibilities of the problem."""
    revealables: RevealableSet
    """The revealables of the problem."""
    initialization: Set[Predicate[Object]]
    """The problem's initialization."""
    goals: GoalList
    """The problem's goal conditions."""

    @classmethod
    def from_raw_parts(
        cls,
        name: Identifier,
        used_domain_name: Identifier,
        requirements: RequirementSet,
        objects: list[Typed[Object]],
        action_fallibilities: ActionFallibilitySet | None,
        revealables: RevealableSet | None,
        initialization: list[Predicate[Object]],
        goal_conditions: GoalList | Condition[Object],
    ) -> "RawProblem":
        """Construct a `RawProblem` from the subnodes returned by a parser."""
        object_types = {}

        for object_ in objects:
            if object_.value in object_types:
                raise ValueError(
                    f"object with name {object_.value} is defined multiple times"  # noqa: E501
                )

            object_types[object_.value] = object_.type

        if (
            action_fallibilities
            and Requirement.FALLIBLE_ACTIONS not in requirements
        ):
            raise ValueError(
                f"{action_fallibilities} defined, but `{Requirement.FALLIBLE_ACTIONS}` does not appear in {requirements}"  # noqa: E501
            )

        if revealables and Requirement.REVEALABLES not in requirements:
            raise ValueError(
                f"{revealables} defined, but `{Requirement.REVEALABLES}` does not appear in {requirements}"  # noqa: E501
            )

        true_predicates = set()

        for predicate in initialization:
            if predicate in true_predicates:
                raise ValueError(
                    f"predicate {predicate} appears in initialization multiple times"  # noqa: E501
                )

            true_predicates.add(predicate)

        if (
            not isinstance(goal_conditions, GoalList)
            and Requirement.MULTIPLE_GOALS not in requirements
        ):
            raise ValueError(
                f"{goal_conditions} defined, but `{Requirement.REVEALABLES}` does not appear in {requirements}"  # noqa: E501
            )

        return RawProblem(
            name,
            used_domain_name,
            requirements,
            object_types,
            action_fallibilities
            if action_fallibilities
            else ActionFallibilitySet(),
            revealables if revealables else RevealableSet(),
            true_predicates,
            goal_conditions
            if isinstance(goal_conditions, GoalList)
            else GoalList([goal_conditions]),
        )


@dataclass(frozen=True)
class Problem:
    """Represents a PDDL problem."""

    raw_problem: RawProblem
    """The backing raw problem."""
    domain: InitVar[Domain]
    """The domain used for validation."""

    @property
    def name(self) -> Identifier:
        """The problem's name."""
        return self.raw_problem.name

    @property
    def used_domain_name(self) -> Identifier:
        """The name of the domain used by the problem."""
        return self.raw_problem.used_domain_name

    @property
    def requirements(self) -> RequirementSet:
        """The problem's requirements."""
        return self.raw_problem.requirements

    @property
    def object_types(self) -> dict[Object, Type]:
        """The objects of the PDDL problem (and their types)."""
        return self.raw_problem.object_types

    @property
    def action_fallibilities(self) -> ActionFallibilitySet:
        """The action fallibilities of the problem."""
        return self.raw_problem.action_fallibilities

    @property
    def revealables(self) -> RevealableSet:
        """The revealables of the problem."""
        return self.raw_problem.revealables

    @property
    def initialization(self) -> Set[Predicate[Object]]:
        """The problem's initialization."""
        return self.raw_problem.initialization

    @property
    def goals(self) -> GoalList:
        """The problem's goal conditions."""
        return self.raw_problem.goals

    def __post_init__(self, domain: Domain) -> None:
        """Validate the problem (e.g., that all referenced predicates exist)."""
        self._validate(domain)

    def _validate_used_domain_name(self, domain: Domain) -> None:
        if domain.name != self.used_domain_name:
            raise ValueError(
                f"used domain name {self.used_domain_name} doesn't match paired domain name {domain.name}"  # noqa: E501
            )

    def _validate_object_types(self, domain: Domain) -> None:
        for object_, type in self.object_types.items():
            if type not in domain.type_hierarchy:
                raise ValueError(
                    f"object {object_} is of an undefined type {type}"
                )

            if object_ in domain.constant_types:
                raise ValueError(
                    f"object with name {object_} is also defined in domain"
                )

    def _validate_action_fallibilities(self, domain: Domain) -> None:
        for fallibility in self.action_fallibilities:
            if fallibility.name not in domain.action_definitions:
                raise ValueError(
                    f"{fallibility} uses an undefined action {fallibility.name}"
                )

            fallibility.condition._validate(
                {},
                ChainMap(self.object_types, domain.constant_types),
                domain.predicate_definitions,
                domain.type_hierarchy,
                domain.requirements,
            )

    def _validate_initialization(self, domain: Domain) -> None:
        for predicate in self.initialization:
            predicate._validate(
                {},
                ChainMap(self.object_types, domain.constant_types),
                domain.predicate_definitions,
                domain.type_hierarchy,
                domain.requirements,
            )

    def _validate_goal_conditions(self, domain: Domain) -> None:
        if (
            len(self.goals) != 1
            and Requirement.MULTIPLE_GOALS not in self.requirements
        ):
            raise ValueError(
                f"number of goals is {len(self.goals)} (not one), but `{Requirement.MULTIPLE_GOALS}` does not appear in {self.requirements}"  # noqa: E501
            )

        for goal_condition in self.goals:
            goal_condition._validate(
                {},
                ChainMap(self.object_types, domain.constant_types),
                domain.predicate_definitions,
                domain.type_hierarchy,
                domain.requirements,
            )

    def _validate(self, domain: Domain) -> None:
        self._validate_used_domain_name(domain)
        self._validate_object_types(domain)
        self._validate_initialization(domain)
        self._validate_goal_conditions(domain)

    @override
    def __repr__(self) -> str:
        # NOTE: We purposefully don't include the revealables and
        # fallible actions, as these are considered hidden information.

        problem_name = f"(problem {self.name!r})"
        used_domain_name = f"(:domain {self.used_domain_name!r})"

        requirements_section = (
            f"(:requirements {' '.join(map(repr, self.requirements))})"
        )

        object_type_pairs = _as_typed_iter(self.object_types)
        objects_section = f"(:objects {' '.join(map(repr, object_type_pairs))})"

        initialization_section = (
            f"(:init {' '.join(map(repr, self.initialization))})"
        )

        goal_section = f"(:goal {' '.join(map(repr, self.goals))})"

        return f"(define {problem_name} {used_domain_name} {requirements_section} {objects_section} {initialization_section} {goal_section})"  # noqa: E501
