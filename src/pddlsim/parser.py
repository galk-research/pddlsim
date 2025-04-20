import bisect
import itertools
import operator
import os
from collections.abc import Iterable, Iterator, Mapping, Set
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from itertools import chain
from random import Random
from typing import cast

from lark import Lark, Token, Transformer, v_args
from pydantic.dataclasses import dataclass as pydantic_dataclass

from pddlsim import _RESOURCES


class Requirement(StrEnum):
    STRIPS = ":strips"
    TYPING = ":typing"
    DISJUNCTIVE_PRECONDITIONS = ":disjunctive-preconditions"
    EQUALITY = ":equality"
    PROBABILISTIC_EFFECTS = ":probabilistic-effects"


@dataclass(eq=True, frozen=True)
class Identifier:
    value: str

    def __str__(self) -> str:
        return self.value


@dataclass(eq=True, order=True, frozen=True)
class Variable:
    value: str

    def __str__(self) -> str:
        return f"?{self.value}"


class CustomType(Identifier):
    pass


@dataclass(eq=True, frozen=True)
class ObjectType:
    pass


type TypeName = CustomType | ObjectType


@dataclass(eq=True, frozen=True)
class ObjectName(Identifier):
    def __str__(self) -> str:
        return self.value


@dataclass(eq=True, frozen=True)
class Typed[T]:
    value: T
    type_name: TypeName


@dataclass(frozen=True)
class PredicateDefinition:
    name: Identifier
    parameters: list[Typed[Variable]]


type Argument = Variable | ObjectName


@dataclass(frozen=True)
class AndCondition[A: Argument]:
    subconditions: list["Condition[A]"]


@dataclass(frozen=True)
class OrCondition[A: Argument]:
    subconditions: list["Condition[A]"]


@dataclass(frozen=True)
class NotCondition[A: Argument]:
    base_condition: "Condition[A]"


@dataclass(frozen=True)
class EqualityCondition[A: Argument]:
    left_side: A
    right_side: A

    def __str__(self) -> str:
        return f"(= {self.left_side} {self.right_side})"


@dataclass(frozen=True)
class Predicate[A: Argument]:
    name: Identifier
    assignment: tuple[A, ...]

    def __str__(self) -> str:
        result = f"({self.name}"

        for argument in self.assignment:
            result += f" {argument}"

        result += ")"

        return result

    @classmethod
    def from_serializable_predicate(
        cls, serializable_predicate: "SerializablePredicate"
    ) -> "Predicate[ObjectName]":
        return Predicate(
            Identifier(serializable_predicate.name),
            tuple(
                ObjectName(object_name)
                for object_name in serializable_predicate.assignment
            ),
        )


@pydantic_dataclass
class SerializablePredicate:
    name: str
    assignment: list[str]

    @classmethod
    def from_predicate(
        cls, predicate: Predicate[ObjectName]
    ) -> "SerializablePredicate":
        return SerializablePredicate(
            predicate.name.value,
            [object_name.value for object_name in predicate.assignment],
        )


type Condition[A: Argument] = (
    AndCondition[A]
    | OrCondition[A]
    | NotCondition[A]
    | Predicate[A]
    | EqualityCondition[A]
)


@dataclass(frozen=True)
class NotPredicate[A: Argument]:
    base_predicate: Predicate[A]


type Atom[A: Argument] = Predicate[A] | NotPredicate[A]


@dataclass(frozen=True)
class AndEffect[A: Argument]:
    subeffects: list["Effect[A]"]


@dataclass(frozen=True)
class ProbabilisticEffect[A: Argument]:
    _possible_effects: list["Effect[A]"]
    _cummulative_probabilities: list[float]

    @classmethod
    def from_possibilities(
        cls, possibilities: list[tuple[float, "Effect[A]"]]
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

    def choose_possibility(self, rng: Random) -> "Effect[A]":
        index = bisect.bisect(self._cummulative_probabilities, rng.random())

        if index == len(self._possible_effects):
            return AndEffect([])  # Empty effect

        return self._possible_effects[index]


type Effect[A: Argument] = AndEffect[A] | ProbabilisticEffect[A] | Atom[A]


@dataclass(frozen=True)
class ActionDefinition:
    name: Identifier
    parameters: list[Typed[Variable]]
    precondition: Condition[Argument]
    effect: Effect[Argument]


@dataclass(frozen=True)
class TypeHierarchy:
    _supertypes: Mapping[CustomType, TypeName]

    @classmethod
    def from_custom_types(
        cls, custom_types: Iterable[Typed[CustomType]]
    ) -> "TypeHierarchy":
        return TypeHierarchy(
            {
                custom_type.value: custom_type.type_name
                for custom_type in custom_types
            }
        )

    def __iter__(self) -> Iterator[Typed[CustomType]]:
        return (
            Typed(subtype, supertype)
            for subtype, supertype in self._supertypes.items()
        )

    def supertype(self, custom_type: CustomType) -> TypeName:
        return self._supertypes[custom_type]


@dataclass(frozen=True)
class Domain:
    name: Identifier
    requirements: Set[Requirement]
    type_hierarchy: TypeHierarchy
    constants: Set[Typed[ObjectName]]
    predicate_definitions: Mapping[Identifier, PredicateDefinition]
    action_definitions: Mapping[Identifier, ActionDefinition]


@dataclass(frozen=True)
class Problem:
    name: Identifier
    used_domain_name: Identifier
    requirements: Set[Requirement]
    objects: Set[Typed[ObjectName]]
    initialization: Set[Predicate[ObjectName]]
    goal_condition: Condition[ObjectName]


@v_args(inline=True)
class PDDLTransformer(Transformer):
    def IDENTIFIER(self, token: Token) -> Identifier:
        return Identifier(str(token))

    def VARIABLE(self, token: Token) -> Variable:
        return Variable(token[1:])

    def NUMBER(self, token: Token) -> Decimal:
        return Decimal(token)

    def strips_requirement(self) -> Requirement:
        return Requirement.STRIPS

    def typing_requirement(self) -> Requirement:
        return Requirement.TYPING

    def disjunctive_preconditions_requirement(self) -> Requirement:
        return Requirement.DISJUNCTIVE_PRECONDITIONS

    def equality_requirement(self) -> Requirement:
        return Requirement.EQUALITY

    def probabilistic_effects(self) -> Requirement:
        return Requirement.PROBABILISTIC_EFFECTS

    @v_args(inline=False)
    def requirements_section(
        self, requirements: list[Requirement]
    ) -> Set[Requirement]:
        return frozenset(requirements)

    def object_type(self) -> ObjectType:
        return ObjectType()

    def custom_type(self, identifier: Identifier) -> CustomType:
        return CustomType(identifier.value)

    @v_args(inline=False)
    def nonempty_list[T](self, items: list[T]) -> Iterable[T]:
        return items

    def typed_list_part[T](
        self, items: Iterable[T], type_name: TypeName
    ) -> Iterable[Typed[T]]:
        return (Typed(item, type_name) for item in items)

    def object_typed_list[T](self, items: Iterable[T]) -> Iterable[Typed[T]]:
        return (Typed(item, ObjectType()) for item in items)

    def typed_list[T](
        self, head: Iterable[Typed[T]], tail: Iterable[Typed[T]] | None
    ) -> Iterable[Typed[T]]:
        return chain(head, tail) if tail else head

    def types_section(self, types: list[Typed[CustomType]]) -> TypeHierarchy:
        return TypeHierarchy.from_custom_types(types)

    def object_name(self, identifier: Identifier) -> ObjectName:
        return ObjectName(identifier.value)

    @v_args(inline=False)
    def constants_section(
        self, objects: list[Typed[ObjectName]]
    ) -> Set[Typed[ObjectName]]:
        return frozenset(objects)

    def predicate_definition(
        self, name: Identifier, parameters: Iterable[Typed[Variable]]
    ) -> PredicateDefinition:
        return PredicateDefinition(name, list(parameters))

    @v_args(inline=False)
    def predicates_section(
        self, predicate_definitions: list[PredicateDefinition]
    ) -> Mapping[Identifier, PredicateDefinition]:
        return {
            predicate_definition.name: predicate_definition
            for predicate_definition in predicate_definitions
        }

    @v_args(inline=False)
    def assignment[A: Argument](self, assignment: list[A]) -> tuple[A, ...]:
        return tuple(assignment)

    def predicate[A: Argument](
        self, name: Identifier, assignment: tuple[A, ...]
    ) -> Predicate[A]:
        return Predicate(name, assignment)

    @v_args(inline=False)
    def and_condition[A: Argument](
        self, operands: list[Condition[A]]
    ) -> AndCondition[A]:
        return AndCondition(operands)

    @v_args(inline=False)
    def or_condition[A: Argument](
        self, operands: list[Condition[A]]
    ) -> OrCondition[A]:
        return OrCondition(operands)

    def not_condition[A: Argument](
        self, operand: Condition[A]
    ) -> NotCondition[A]:
        return NotCondition(operand)

    def equality_condition[A: Argument](
        self, left_side: A, right_side: A
    ) -> EqualityCondition[A]:
        return EqualityCondition(left_side, right_side)

    def not_predicate[A: Argument](
        self, base_predicate: Predicate[A]
    ) -> NotPredicate[A]:
        return NotPredicate(base_predicate)

    @v_args(inline=False)
    def and_effect[A: Argument](
        self, subeffects: list[Effect[A]]
    ) -> AndEffect[A]:
        return AndEffect(subeffects)

    def probabilistic_effect_pair[A: Argument](
        self, probability: float, effect: Effect[A]
    ) -> tuple[float, Effect[A]]:
        if not (0 <= probability <= 1):
            raise ValueError(
                f"probability must be between 0 and 1, is {probability}"
            )

        return (probability, effect)

    @v_args(inline=False)
    def probabilistic_effect[A: Argument](
        self, possibilities: list[tuple[float, Effect[A]]]
    ) -> ProbabilisticEffect:
        return ProbabilisticEffect.from_possibilities(possibilities)

    def action_definition(
        self,
        name: Identifier,
        parameters: Iterable[Typed[Variable]],
        precondition: Condition[Argument] | None,
        effect: Effect[Argument] | None,
    ) -> ActionDefinition:
        return ActionDefinition(
            name,
            list(parameters),
            precondition if precondition else AndCondition([]),
            effect if effect else AndEffect([]),
        )

    @v_args(inline=False)
    def actions_section(
        self, action_definitions: list[ActionDefinition]
    ) -> Mapping[Identifier, ActionDefinition]:
        return {
            action_definition.name: action_definition
            for action_definition in action_definitions
        }

    def domain(
        self,
        name: Identifier,
        requirements: Set[Requirement] | None,
        type_hierarchy: TypeHierarchy | None,
        constants: Set[Typed[ObjectName]] | None,
        predicate_definitions: Mapping[Identifier, PredicateDefinition] | None,
        action_definitions: Mapping[Identifier, ActionDefinition] | None,
    ) -> Domain:
        return Domain(
            name,
            requirements if requirements else frozenset(),
            type_hierarchy
            if type_hierarchy
            else TypeHierarchy.from_custom_types([]),
            constants if constants else frozenset(),
            predicate_definitions if predicate_definitions else {},
            action_definitions if action_definitions else {},
        )

    def objects_section(
        self, objects: Iterable[Typed[ObjectName]]
    ) -> Set[Typed[ObjectName]]:
        return frozenset(objects)

    @v_args(inline=False)
    def initialization_section(
        self, predicates: list[Predicate[ObjectName]]
    ) -> Set[Predicate[ObjectName]]:
        return frozenset(predicates)

    def problem(
        self,
        name: Identifier,
        used_domain_name: Identifier,
        requirements: Set[Requirement] | None,
        objects: Set[Typed[ObjectName]] | None,
        initialization: Set[Predicate[ObjectName]],
        goal_condition: Condition[ObjectName],
    ) -> Problem:
        return Problem(
            name,
            used_domain_name,
            requirements if requirements else frozenset(),
            objects if objects else frozenset(),
            initialization,
            goal_condition,
        )


# Cache the parser for each invocation, and persist it
_PDDL_PARSER = Lark(
    _RESOURCES.joinpath("grammar.lark").read_text(),
    parser="lalr",
    cache=True,
    transformer=PDDLTransformer(),
    start=["domain", "problem"],
)


def parse_domain(text: str) -> Domain:
    return cast(Domain, _PDDL_PARSER.parse(text, "domain"))


def parse_problem(text: str) -> Problem:
    return cast(Problem, _PDDL_PARSER.parse(text, "problem"))


def parse_domain_from_file(path: str | os.PathLike) -> Domain:
    with open(path) as file:
        return parse_domain(file.read())


def parse_problem_from_file(path: str | os.PathLike) -> Problem:
    with open(path) as file:
        return parse_problem(file.read())
