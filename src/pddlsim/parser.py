import pathlib
import pprint
from collections.abc import Iterable, Mapping, Sequence, Set
from dataclasses import dataclass
from enum import StrEnum

from lark import Lark, Token, Transformer, v_args


class Requirement(StrEnum):
    STRIPS = ":strips"
    TYPING = ":typing"
    DISJUNCTIVE_PRECONDITIONS = ":disjunctive-preconditions"


@dataclass(eq=True, frozen=True)
class Identifier:
    value: str


@dataclass(frozen=True)
class Variable:
    value: str


@dataclass(frozen=True)
class PredicateDefinition:
    name: Identifier
    parameters: Sequence[Variable]


type Argument = Variable | Identifier


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
class Predicate[A: Argument]:
    name: Identifier
    assignment: Sequence[A]


type Condition[A: Argument] = (
    AndCondition[A] | OrCondition[A] | NotCondition[A] | Predicate[A]
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
    parameters: Sequence[Variable]
    precondition: Condition[Argument]
    effect: Effect[Argument]


@dataclass(frozen=True)
class Domain:
    name: Identifier
    requirements: Set[Requirement]
    constants: Set[Identifier]
    predicate_definitions: Mapping[Identifier, PredicateDefinition]
    action_definitions: Mapping[Identifier, ActionDefinition]


@dataclass(frozen=True)
class Problem:
    name: Identifier
    used_domain_name: Identifier
    requirements: Set[Requirement]
    objects: Set[Identifier]
    initialization: Set[Predicate[Identifier]]
    goal_condition: Condition[Identifier]


@v_args(inline=True)
class PDDLTransformer(Transformer):
    def IDENTIFIER(self, token: Token) -> Identifier:
        return Identifier(str(token))

    def VARIABLE(self, token: Token) -> Variable:
        return Variable(token[1:])

    @v_args(inline=False)
    def variables(self, variables: Iterable[Variable]) -> Sequence[Variable]:
        return tuple(variables)

    def strips_requirement(self) -> Requirement:
        return Requirement.STRIPS

    def typing_requirement(self) -> Requirement:
        return Requirement.TYPING

    def disjunctive_preconditions_requirement(self) -> Requirement:
        return Requirement.DISJUNCTIVE_PRECONDITIONS

    @v_args(inline=False)
    def requirements_section(
        self, requirements: Iterable[Requirement]
    ) -> Set[Requirement]:
        return frozenset(requirements)

    @v_args(inline=False)
    def constants_section(
        self, objects: Iterable[Identifier]
    ) -> Set[Identifier]:
        return frozenset(objects)

    def predicate_definition(
        self, name: Identifier, parameters: Sequence[Variable]
    ) -> PredicateDefinition:
        return PredicateDefinition(name, parameters)

    @v_args(inline=False)
    def predicates_section(
        self, predicate_definitions: Iterable[PredicateDefinition]
    ) -> Mapping[Identifier, PredicateDefinition]:
        return {
            predicate_definition.name: predicate_definition
            for predicate_definition in predicate_definitions
        }

    @v_args(inline=False)
    def assignment(self, assignment: Iterable[Argument]) -> Sequence[Argument]:
        return tuple(assignment)

    def predicate(
        self, name: Identifier, assignment: Sequence[Argument]
    ) -> Predicate[Argument]:
        return Predicate(name, assignment)

    @v_args(inline=False)
    def and_condition(
        self, operands: Iterable[Condition[Argument]]
    ) -> AndCondition[Argument]:
        return AndCondition(tuple(operands))

    @v_args(inline=False)
    def or_condition(
        self, operands: Iterable[Condition[Argument]]
    ) -> OrCondition[Argument]:
        return OrCondition(tuple(operands))

    def not_condition(
        self, operand: Condition[Argument]
    ) -> NotCondition[Argument]:
        return NotCondition(operand)

    def not_predicate(
        self, base_predicate: Predicate[Argument]
    ) -> NotPredicate[Argument]:
        return NotPredicate(base_predicate)

    def atom_effect(self, atom: Atom[Argument]) -> AndEffect[Argument]:
        return AndEffect([atom])

    @v_args(inline=False)
    def and_effect(
        self, atoms: Iterable[Atom[Argument]]
    ) -> AndEffect[Argument]:
        return AndEffect(tuple(atoms))

    def action_definition(
        self,
        name: Identifier,
        parameters: Sequence[Variable],
        precondition: Condition[Argument] | None,
        effect: Effect[Argument] | None,
    ) -> ActionDefinition:
        return ActionDefinition(
            name,
            parameters,
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
        constants: Set[Identifier] | None,
        predicate_definitions: Mapping[Identifier, PredicateDefinition] | None,
        action_definitions: Mapping[Identifier, ActionDefinition] | None,
    ) -> Domain:
        return Domain(
            name,
            requirements if requirements else frozenset(),
            constants if constants else frozenset(),
            predicate_definitions if predicate_definitions else {},
            action_definitions if action_definitions else {},
        )

    @v_args(inline=False)
    def objects_section(self, objects: Iterable[Identifier]) -> Set[Identifier]:
        return frozenset(objects)

    @v_args(inline=False)
    def initialization_section(
        self, predicates: Iterable[Predicate[Identifier]]
    ) -> Set[Predicate[Identifier]]:
        return frozenset(predicates)

    def problem(
        self,
        name: Identifier,
        used_domain_name: Identifier,
        requirements: Set[Requirement] | None,
        objects: Set[Identifier] | None,
        initialization: Set[Predicate[Identifier]],
        goal_condition: Condition[Identifier],
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

    with open("instance.pddl") as problem_file:
        pprint.pprint(parse_problem(problem_file.read()))
