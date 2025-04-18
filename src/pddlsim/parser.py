import bisect
import itertools
import operator
import os
import pathlib
from collections.abc import Iterable, Iterator, Mapping, Set
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from itertools import chain
from random import Random
from typing import cast

from lark import Lark, Token, Transformer, v_args

from pddlsim.asp import ID, IDAllocator, IDKind


class Requirement(StrEnum):
    STRIPS = ":strips"
    TYPING = ":typing"
    DISJUNCTIVE_PRECONDITIONS = ":disjunctive-preconditions"
    EQUALITY = ":equality"
    PROBABILISTIC_EFFECTS = ":probabilistic-effects"


@dataclass(eq=True, frozen=True)
class Identifier:
    value: str

    def __repr__(self) -> str:
        return self.value


@dataclass(eq=True, order=True, frozen=True)
class Variable:
    value: str

    def __repr__(self) -> str:
        return f"?{self.value}"


class CustomType(Identifier):
    pass


@dataclass(eq=True, frozen=True)
class ObjectType:
    pass


type TypeName = CustomType | ObjectType


@dataclass(eq=True, frozen=True)
class ObjectName(Identifier):
    def __repr__(self) -> str:
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

    def __repr__(self) -> str:
        return f"(= {repr(self.left_side)} {repr(self.right_side)})"


@dataclass(frozen=True)
class Predicate[A: Argument]:
    name: Identifier
    assignment: list[A]

    def __repr__(self) -> str:
        result = f"({repr(self.name)}"

        for argument in self.assignment:
            result += f" {repr(argument)}"

        result += ")"

        return result


type Primitive[A: Argument] = Predicate[A] | EqualityCondition[A]


type Condition[A: Argument] = (
    AndCondition[A] | OrCondition[A] | NotCondition[A] | Primitive[A]
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
            return AndEffect([])

        return self._possible_effects[index]


type Effect[A: Argument] = AndEffect[A] | ProbabilisticEffect[A] | Atom[A]


@dataclass(frozen=True)
class ActionDefinition:
    name: Identifier
    parameters: list[Typed[Variable]]
    precondition: Condition[Argument]
    effect: Effect[Argument]

    def _parameters_as_asp_part(
        self,
        variable_id_allocator: IDAllocator[Variable],
        type_name_id_allocator: IDAllocator[TypeName],
    ) -> str:
        result = []

        for parameter in self.parameters:
            variable = parameter.value
            type_name = parameter.type_name

            variable_id = variable_id_allocator.get_id_or_insert(variable)
            type_name_id = type_name_id_allocator.get_id_or_insert(type_name)

            result.append(f"1 {{ {variable_id}(O) : {type_name_id}(O) }} 1.")

        return "\n".join(result)

    def _precondition_as_asp_part(
        self,
        variable_id_allocator: IDAllocator[Variable],
        object_name_id_allocator: IDAllocator[ObjectName],
        predicate_id_allocator: IDAllocator[Identifier],
    ) -> str:
        result = []

        rule_id_allocator = IDAllocator[None](IDKind.RULE)

        def condition_to_asp_part(condition: Condition) -> ID:
            temporary_id_allocator = IDAllocator[Variable](IDKind.TEMPORARY)

            def argument_to_id(argument: Argument) -> ID:
                match argument:
                    case Variable():
                        temporary_id = temporary_id_allocator.get_id_or_insert(
                            argument
                        )
                        return temporary_id
                    case ObjectName():
                        return object_name_id_allocator.get_id_or_insert(
                            argument
                        )

            rule_id = rule_id_allocator.next_id()

            match condition:
                case AndCondition(subconditions):
                    subcondition_ids = (
                        condition_to_asp_part(subcondition)
                        for subcondition in subconditions
                    )

                    result.append(
                        f"{rule_id} :- {
                            ', '.join(
                                f'{subcondition_id}'
                                for subcondition_id in subcondition_ids
                            )
                        }."
                    )
                case OrCondition(subconditions):
                    for subcondition in subconditions:
                        subcondition_id = condition_to_asp_part(subcondition)

                        result.append(f"{rule_id} :- {subcondition_id}.")
                case NotCondition(base_condition):
                    base_condition_id = condition_to_asp_part(base_condition)

                    result.append(f"{rule_id} :- not {base_condition_id}.")
                case Predicate(name=name, assignment=assignment):
                    predicate_id = predicate_id_allocator.get_id_or_insert(name)
                    arguments = (
                        str(argument_to_id(argument)) for argument in assignment
                    )

                    body = [f"{predicate_id}({', '.join(arguments)})"]

                    for variable, temporary_id in temporary_id_allocator:
                        variable_id = variable_id_allocator.get_id_or_insert(
                            variable
                        )
                        body.append(f"{variable_id}({temporary_id})")

                    result.append(f"{rule_id} :- {', '.join(body)}.")
                case EqualityCondition(
                    left_side=left_side, right_side=right_side
                ):
                    left_side_id = argument_to_id(left_side)
                    right_side_id = argument_to_id(right_side)
                    body = [f"{left_side_id} == {right_side_id}"]

                    for variable, temporary_id in temporary_id_allocator:
                        variable_id = variable_id_allocator.get_id_or_insert(
                            variable
                        )
                        body.append(f"{variable_id}({temporary_id})")

                    result.append(f"{rule_id} :- {', '.join(body)}.")

            return rule_id

        condition_rule_id = condition_to_asp_part(self.precondition)
        result.append(f":- not {condition_rule_id}.")

        for _, id in variable_id_allocator:
            result.append(f"#show {id}/1.")

        return "\n".join(result)

    def _as_asp_program(
        self,
        variable_id_allocator: IDAllocator[Variable],
        object_name_id_allocator: IDAllocator[ObjectName],
        predicate_id_allocator: IDAllocator[Identifier],
        type_name_id_allocator: IDAllocator[TypeName],
    ) -> str:
        parameters_part = self._parameters_as_asp_part(
            variable_id_allocator, type_name_id_allocator
        )
        precondition_part = self._precondition_as_asp_part(
            variable_id_allocator,
            object_name_id_allocator,
            predicate_id_allocator,
        )

        return f"{parameters_part}\n{precondition_part}"


class TypeHierarchy:
    def __init__(self, custom_types: Iterable[Typed[CustomType]]) -> None:
        self._hierarchy = {
            custom_type.value: custom_type.type_name
            for custom_type in custom_types
        }

    def __iter__(self) -> Iterator[Typed[CustomType]]:
        return (
            Typed(subtype, supertype)
            for subtype, supertype in self._hierarchy.items()
        )

    def supertype(self, custom_type: CustomType) -> TypeName:
        return self._hierarchy[custom_type]

    def __repr__(self) -> str:
        return repr(self._hierarchy)


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
        return TypeHierarchy(types)

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
    def assignment[A: Argument](self, assignment: list[A]) -> list[A]:
        return assignment

    def predicate[A: Argument](
        self, name: Identifier, assignment: list[A]
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
            type_hierarchy if type_hierarchy else TypeHierarchy(iter(())),
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


with open(pathlib.Path(__file__).parent / "grammar.lark") as grammar_file:
    _PDDL_PARSER = Lark(
        grammar_file.read(),
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
