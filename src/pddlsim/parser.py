import pathlib
import pprint
from collections.abc import Iterable, Mapping, Sequence, Set
from dataclasses import dataclass
from enum import StrEnum
from itertools import chain

from lark import Lark, Token, Transformer, v_args


class Requirement(StrEnum):
    STRIPS = ":strips"
    TYPING = ":typing"
    DISJUNCTIVE_PRECONDITIONS = ":disjunctive-preconditions"
    EQUALITY = ":equality"


class Identifier(str):
    pass


class Variable(str):
    pass


class CustomType(Identifier):
    pass


@dataclass(eq=True, frozen=True)
class ObjectType:
    pass


type TypeName = CustomType | ObjectType


class ObjectName(Identifier):
    pass


@dataclass(eq=True, frozen=True)
class Typed[T]:
    value: T
    type_name: TypeName


@dataclass(frozen=True)
class PredicateDefinition:
    name: Identifier
    parameters: Sequence[Typed[Variable]]


type Argument = Variable | ObjectName


@dataclass(frozen=True)
class AndCondition[A: Argument]:
    operands: Sequence["Condition[A]"]


@dataclass(frozen=True)
class OrCondition[A: Argument]:
    operands: Sequence["Condition[A]"]


@dataclass(frozen=True)
class NotCondition[A: Argument]:
    operand: "Condition[A]"


@dataclass(frozen=True)
class EqualityCondition[A: Argument]:
    left_side: A
    right_side: A


@dataclass(frozen=True)
class Predicate[A: Argument]:
    name: Identifier
    assignment: Sequence[A]


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


type Atom[A: Argument] = Predicate[A] | NotPredicate[A]


@dataclass(frozen=True)
class AndEffect[A: Argument]:
    atoms: Sequence[Atom[A]]


type Effect[A: Argument] = AndEffect[A] | Atom[A]


@dataclass(frozen=True)
class ActionDefinition:
    name: Identifier
    parameters: Sequence[Typed[Variable]]
    precondition: Condition[Argument]
    effect: Effect[Argument]


class TypeHierarchy:
    def __init__(self, custom_types: Iterable[Typed[CustomType]]) -> None:
        self._hierarchy = {
            custom_type.value: custom_type.type_name
            for custom_type in custom_types
        }

    def supertype(self, custom_type: CustomType) -> TypeName:
        return self._hierarchy[custom_type]

    def __repr__(self) -> str:
        return repr(self._hierarchy)


@dataclass(frozen=True)
class Domain:
    name: Identifier
    requirements: Set[Requirement]
    types: TypeHierarchy
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

    def strips_requirement(self) -> Requirement:
        return Requirement.STRIPS

    def typing_requirement(self) -> Requirement:
        return Requirement.TYPING

    def disjunctive_preconditions_requirement(self) -> Requirement:
        return Requirement.DISJUNCTIVE_PRECONDITIONS

    def equality_requirement(self) -> Requirement:
        return Requirement.EQUALITY

    @v_args(inline=False)
    def requirements_section(
        self, requirements: Iterable[Requirement]
    ) -> Set[Requirement]:
        return frozenset(requirements)

    def object_type(self) -> ObjectType:
        return ObjectType()

    def custom_type(self, identifier: Identifier) -> CustomType:
        return CustomType(identifier)

    @v_args(inline=False)
    def nonempty_list[T](self, items: Iterable[T]) -> Iterable[T]:
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

    def types_section(
        self, types: Iterable[Typed[CustomType]]
    ) -> TypeHierarchy:
        return TypeHierarchy(types)

    def object_name(self, identifier: Identifier) -> ObjectName:
        return ObjectName(identifier)

    @v_args(inline=False)
    def constants_section(
        self, objects: Iterable[Typed[ObjectName]]
    ) -> Set[Typed[ObjectName]]:
        return frozenset(objects)

    def predicate_definition(
        self, name: Identifier, parameters: Iterable[Typed[Variable]]
    ) -> PredicateDefinition:
        return PredicateDefinition(name, tuple(parameters))

    @v_args(inline=False)
    def predicates_section(
        self, predicate_definitions: Iterable[PredicateDefinition]
    ) -> Mapping[Identifier, PredicateDefinition]:
        return {
            predicate_definition.name: predicate_definition
            for predicate_definition in predicate_definitions
        }

    @v_args(inline=False)
    def assignment[A: Argument](self, assignment: Iterable[A]) -> Iterable[A]:
        return assignment

    def predicate[A: Argument](
        self, name: Identifier, assignment: Sequence[A]
    ) -> Predicate[A]:
        return Predicate(name, assignment)

    @v_args(inline=False)
    def and_condition[A: Argument](
        self, operands: Iterable[Condition[A]]
    ) -> AndCondition[A]:
        return AndCondition(tuple(operands))

    @v_args(inline=False)
    def or_condition[A: Argument](
        self, operands: Iterable[Condition[A]]
    ) -> OrCondition[A]:
        return OrCondition(tuple(operands))

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

    def atom_effect[A: Argument](self, atom: Atom[A]) -> AndEffect[A]:
        return AndEffect([atom])

    @v_args(inline=False)
    def and_effect[A: Argument](self, atoms: Iterable[Atom[A]]) -> AndEffect[A]:
        return AndEffect(tuple(atoms))

    def action_definition(
        self,
        name: Identifier,
        parameters: Iterable[Typed[Variable]],
        precondition: Condition[Argument] | None,
        effect: Effect[Argument] | None,
    ) -> ActionDefinition:
        return ActionDefinition(
            name,
            tuple(parameters),
            precondition if precondition else AndCondition([]),
            effect if effect else AndEffect([]),
        )

    @v_args(inline=False)
    def actions_section(
        self, action_definitions: Iterable[ActionDefinition]
    ) -> Mapping[Identifier, ActionDefinition]:
        return {
            action_definition.name: action_definition
            for action_definition in action_definitions
        }

    def domain(
        self,
        name: Identifier,
        requirements: Set[Requirement] | None,
        types: TypeHierarchy | None,
        constants: Set[Typed[ObjectName]] | None,
        predicate_definitions: Mapping[Identifier, PredicateDefinition] | None,
        action_definitions: Mapping[Identifier, ActionDefinition] | None,
    ) -> Domain:
        return Domain(
            name,
            requirements if requirements else frozenset(),
            types if types else TypeHierarchy(iter(())),
            constants if constants else frozenset(),
            predicate_definitions if predicate_definitions else {},
            action_definitions if action_definitions else {},
        )

    @v_args(inline=False)
    def objects_section(
        self, objects: Iterable[Typed[ObjectName]]
    ) -> Set[Typed[ObjectName]]:
        return frozenset(objects)

    @v_args(inline=False)
    def initialization_section(
        self, predicates: Iterable[Predicate[ObjectName]]
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
    return _PDDL_PARSER.parse(text, "domain")  # type: ignore


def parse_problem(text: str) -> Problem:
    return _PDDL_PARSER.parse(text, "problem")  # type: ignore


if __name__ == "__main__":
    with open("domain.pddl") as domain_file:
        pprint.pprint(parse_domain(domain_file.read()))
