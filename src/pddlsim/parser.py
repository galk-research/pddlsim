import os
from collections.abc import Iterable
from decimal import Decimal
from itertools import chain
from typing import cast

from lark import Lark, Token, Transformer, v_args

from pddlsim import _RESOURCES
from pddlsim.ast import (
    ActionDefinition,
    AndCondition,
    AndEffect,
    Argument,
    Condition,
    CustomType,
    Domain,
    Effect,
    EqualityCondition,
    Identifier,
    NotCondition,
    NotPredicate,
    Object,
    ObjectType,
    OrCondition,
    Predicate,
    PredicateDefinition,
    ProbabilisticEffect,
    Problem,
    RawProblemParts,
    Requirement,
    Type,
    Typed,
    TypeHierarchy,
    Variable,
)


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
    ) -> list[Requirement]:
        return requirements

    def object_type(self) -> ObjectType:
        return ObjectType()

    def custom_type(self, identifier: Identifier) -> CustomType:
        return CustomType(identifier.value)

    @v_args(inline=False)
    def nonempty_list[T](self, items: list[T]) -> Iterable[T]:
        return items

    def typed_list_part[T](
        self, items: Iterable[T], type: Type
    ) -> Iterable[Typed[T]]:
        return (Typed(item, type) for item in items)

    def object_typed_list[T](self, items: Iterable[T]) -> Iterable[Typed[T]]:
        return (Typed(item, ObjectType()) for item in items)

    def typed_list[T](
        self, head: Iterable[Typed[T]], tail: Iterable[Typed[T]] | None
    ) -> Iterable[Typed[T]]:
        return chain(head, tail) if tail else head

    def types_section(self, types: list[Typed[CustomType]]) -> TypeHierarchy:
        return TypeHierarchy.from_raw_parts(types)

    def object_(self, identifier: Identifier) -> Object:
        return Object(identifier.value)

    @v_args(inline=False)
    def constants_section(
        self, objects: list[Typed[Object]]
    ) -> list[Typed[Object]]:
        return objects

    def predicate_definition(
        self, name: Identifier, parameters: Iterable[Typed[Variable]]
    ) -> PredicateDefinition:
        return PredicateDefinition.from_raw_parts(name, list(parameters))

    @v_args(inline=False)
    def predicates_section(
        self, predicate_definitions: list[PredicateDefinition]
    ) -> list[PredicateDefinition]:
        return predicate_definitions

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
        self, probability: Decimal, effect: Effect[A]
    ) -> tuple[Decimal, Effect[A]]:
        if not (0 <= probability <= 1):
            raise ValueError(
                f"probability must be between 0 and 1, is {probability}"
            )

        return (probability, effect)

    @v_args(inline=False)
    def probabilistic_effect[A: Argument](
        self, possibilities: list[tuple[Decimal, Effect[A]]]
    ) -> ProbabilisticEffect:
        return ProbabilisticEffect.from_possibilities(possibilities)

    def action_definition(
        self,
        name: Identifier,
        parameters: Iterable[Typed[Variable]],
        precondition: Condition[Argument] | None,
        effect: Effect[Argument] | None,
    ) -> ActionDefinition:
        return ActionDefinition.from_raw_parts(
            name,
            list(parameters),
            precondition if precondition else AndCondition([]),
            effect if effect else AndEffect([]),
        )

    @v_args(inline=False)
    def actions_section(
        self, action_definitions: list[ActionDefinition]
    ) -> list[ActionDefinition]:
        return action_definitions

    def domain(
        self,
        name: Identifier,
        requirements: list[Requirement] | None,
        type_hierarchy: TypeHierarchy | None,
        constants: list[Typed[Object]] | None,
        predicate_definitions: list[PredicateDefinition] | None,
        action_definitions: list[ActionDefinition] | None,
    ) -> Domain:
        return Domain.from_raw_parts(
            name,
            requirements if requirements else [],
            type_hierarchy
            if type_hierarchy
            else TypeHierarchy.from_raw_parts([]),
            constants if constants else [],
            predicate_definitions if predicate_definitions else [],
            action_definitions if action_definitions else [],
        )

    def objects_section(
        self, objects: list[Typed[Object]]
    ) -> list[Typed[Object]]:
        return objects

    @v_args(inline=False)
    def initialization_section(
        self, predicates: list[Predicate[Object]]
    ) -> list[Predicate[Object]]:
        return predicates

    def problem(
        self,
        name: Identifier,
        used_domain_name: Identifier,
        objects: list[Typed[Object]] | None,
        initialization: list[Predicate[Object]],
        goal_condition: Condition[Object],
    ) -> RawProblemParts:
        return RawProblemParts(
            name,
            used_domain_name,
            objects if objects else [],
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


def parse_problem(text: str, domain: Domain) -> Problem:
    return Problem.from_raw_parts(
        cast(RawProblemParts, _PDDL_PARSER.parse(text, "problem")), domain
    )


def parse_domain_problem_pair(
    domain_text: str, problem_text: str
) -> tuple[Domain, Problem]:
    domain = parse_domain(domain_text)
    problem = parse_problem(problem_text, domain)

    return (domain, problem)


def parse_domain_from_file(path: str | os.PathLike) -> Domain:
    with open(path) as file:
        return parse_domain(file.read())


def parse_problem_from_file(path: str | os.PathLike, domain: Domain) -> Problem:
    with open(path) as file:
        return parse_problem(file.read(), domain)


def parse_domain_problem_pair_from_file(
    domain_path: str | os.PathLike, problem_path: str | os.PathLike
) -> tuple[Domain, Problem]:
    domain = parse_domain_from_file(domain_path)
    problem = parse_problem_from_file(problem_path, domain)

    return (domain, problem)
