"""Contains utilities to construct `Domain` and `Problem` objects from text."""

import os
from collections.abc import Iterable
from decimal import Decimal
from itertools import chain
from typing import cast

from lark import Lark, Token, Transformer, v_args

from pddlsim import _RESOURCES
from pddlsim.ast import (
    ActionDefinition,
    ActionFallibility,
    ActionFallibilitySet,
    AndCondition,
    AndEffect,
    Argument,
    Condition,
    CustomType,
    Domain,
    Effect,
    EqualityCondition,
    FileLocation,
    GoalList,
    Identifier,
    Location,
    NotCondition,
    NotPredicate,
    Object,
    ObjectType,
    OrCondition,
    Predicate,
    PredicateDefinition,
    ProbabilisticEffect,
    Problem,
    RawProblem,
    Requirement,
    RequirementSet,
    Revealable,
    RevealableSet,
    Type,
    Typed,
    TypeHierarchy,
    Variable,
)


@v_args(inline=True)
class _PDDLTransformer(Transformer):
    def NUMBER(self, token: Token) -> Decimal:  # noqa: N802
        return Decimal(token)

    def IDENTIFIER(self, token: Token) -> Identifier:  # noqa: N802
        return Identifier(str(token), location=FileLocation._from_token(token))

    def VARIABLE(self, token: Token) -> Variable:  # noqa: N802
        return Variable(token[1:], location=FileLocation._from_token(token))

    @v_args(inline=False)
    def list_[T](self, items: list[T]) -> list[T]:
        return items

    @v_args(inline=False)
    def nonempty_list[T](self, items: list[T]) -> list[T]:
        return items

    def strips_requirement(self) -> Requirement:
        return Requirement.STRIPS

    def typing_requirement(self) -> Requirement:
        return Requirement.TYPING

    def disjunctive_preconditions_requirement(self) -> Requirement:
        return Requirement.DISJUNCTIVE_PRECONDITIONS

    def negative_preconditions_requirement(self) -> Requirement:
        return Requirement.NEGATIVE_PRECONDITIONS

    def equality_requirement(self) -> Requirement:
        return Requirement.EQUALITY

    def probabilistic_effects(self) -> Requirement:
        return Requirement.PROBABILISTIC_EFFECTS

    def fallible_actions_requirement(self) -> Requirement:
        return Requirement.FALLIBLE_ACTIONS

    def revealables_requirement(self) -> Requirement:
        return Requirement.REVEALABLES

    def multiple_goals_requirement(self) -> Requirement:
        return Requirement.MULTIPLE_GOALS

    def REQUIREMENTS_KEYWORD(self, token: Token) -> Location:  # noqa: N802
        return FileLocation._from_token(token)

    def requirements_section(
        self, location: Location, requirements: list[Requirement]
    ) -> RequirementSet:
        return RequirementSet.from_raw_parts(requirements, location=location)

    def object_type(self) -> ObjectType:
        return ObjectType()

    def custom_type(self, identifier: Identifier) -> CustomType:
        return CustomType(identifier.value, location=identifier.location)

    def typed_list_part[T](
        self, items: list[T], type: Type
    ) -> Iterable[Typed[T]]:
        return (Typed(item, type) for item in items)

    def object_typed_list[T](self, items: Iterable[T]) -> Iterable[Typed[T]]:
        return (Typed(item, ObjectType()) for item in items)

    def typed_list[T](
        self,
        head: Iterable[Typed[T]],
        tail: Iterable[Typed[T]] | None,
    ) -> Iterable[Typed[T]]:
        return chain(head, tail) if tail else head

    def TYPES_KEYWORD(self, token: Token) -> Location:  # noqa: N802
        return FileLocation._from_token(token)

    def types_section(
        self, location: Location, types: Iterable[Typed[CustomType]]
    ) -> TypeHierarchy:
        return TypeHierarchy.from_raw_parts(types, location=location)

    def object_(self, identifier: Identifier) -> Object:
        return Object(identifier.value, location=identifier.location)

    def constants_section(
        self, objects: list[Typed[Object]]
    ) -> list[Typed[Object]]:
        return objects

    def predicate_definition(
        self,
        name: Identifier,
        parameters: Iterable[Typed[Variable]],
    ) -> PredicateDefinition:
        return PredicateDefinition.from_raw_parts(name, list(parameters))

    def predicates_section(
        self,
        predicate_definitions: list[PredicateDefinition],
    ) -> list[PredicateDefinition]:
        return predicate_definitions

    def predicate[A: Argument](
        self,
        name: Identifier,
        assignment: list[A],
    ) -> Predicate[A]:
        return Predicate(name, tuple(assignment))

    def and_condition[A: Argument](
        self, operands: list[Condition[A]]
    ) -> AndCondition[A]:
        return AndCondition(operands)

    def OR_KEYWORD(self, token: Token) -> Location:  # noqa: N802
        return FileLocation._from_token(token)

    def or_condition[A: Argument](
        self, location: Location, operands: list[Condition[A]]
    ) -> OrCondition[A]:
        return OrCondition(operands, location=location)

    def NOT_KEYWORD(self, token: Token) -> Location:  # noqa: N802
        return FileLocation._from_token(token)

    def not_condition[A: Argument](
        self, location: Location, operand: Condition[A]
    ) -> NotCondition[A]:
        return NotCondition(operand, location=location)

    def EQUALS_SIGN(self, token: Token) -> Location:  # noqa: N802
        return FileLocation._from_token(token)

    def equality_condition[A: Argument](
        self,
        location: Location,
        left_side: A,
        right_side: A,
    ) -> EqualityCondition[A]:
        return EqualityCondition(left_side, right_side, location=location)

    def not_predicate[A: Argument](
        self, base_predicate: Predicate[A]
    ) -> NotPredicate[A]:
        return NotPredicate(base_predicate)

    def and_effect[A: Argument](
        self, subeffects: list[Effect[A]]
    ) -> AndEffect[A]:
        return AndEffect(subeffects)

    def probabilistic_effect_pair[A: Argument](
        self, probability: Decimal, effect: Effect[A]
    ) -> tuple[Decimal, Effect[A]]:
        return (probability, effect)

    def PROBABILISTIC_KEYWORD(self, token: Token) -> Location:  # noqa: N802
        return FileLocation._from_token(token)

    def probabilistic_effect[A: Argument](
        self,
        location: Location,
        possibilities: list[tuple[Decimal, Effect[A]]],
    ) -> ProbabilisticEffect:
        return ProbabilisticEffect.from_possibilities(
            possibilities, location=location
        )

    def action_definition(
        self,
        name: Identifier,
        parameters: list[Typed[Variable]],
        precondition: Condition[Argument] | None,
        effect: Effect[Argument] | None,
    ) -> ActionDefinition:
        return ActionDefinition.from_raw_parts(
            name,
            list(parameters),
            precondition if precondition else AndCondition([]),
            effect if effect else AndEffect([]),
        )

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
            requirements if requirements else RequirementSet({}),  # type: ignore
            type_hierarchy,
            constants if constants else [],
            predicate_definitions if predicate_definitions else [],
            action_definitions if action_definitions else [],
        )

    def objects_section(
        self, objects: list[Typed[Object]]
    ) -> list[Typed[Object]]:
        return objects

    def action_fallibility(
        self,
        action_name: Identifier,
        with_probability: Decimal | None,
        condition: Condition[Object],
    ) -> ActionFallibility:
        return ActionFallibility(
            action_name,
            condition,
            with_probability if with_probability else Decimal(value=1),
        )

    def FAIL_KEYWORD(self, token: Token) -> Location:  # noqa: N802
        return FileLocation._from_token(token)

    def action_fallibilities_section(
        self, location: Location, fallibilities: list[ActionFallibility]
    ) -> ActionFallibilitySet:
        return ActionFallibilitySet.from_raw_parts(
            fallibilities, location=location
        )

    def revealable(
        self,
        with_probability: Decimal | None,
        condition: Condition[Object],
        effect: Effect[Object],
    ) -> Revealable:
        return Revealable(
            effect,
            condition,
            with_probability if with_probability else Decimal(value=1),
        )

    def REVEAL_KEYWORD(self, token: Token) -> Location:  # noqa: N802
        return FileLocation._from_token(token)

    def revealables_section(
        self, location: Location, revealables: list[Revealable]
    ) -> RevealableSet:
        return RevealableSet.from_raw_parts(revealables, location=location)

    def initialization_section(
        self, predicates: list[Predicate[Object]]
    ) -> list[Predicate[Object]]:
        return predicates

    def GOALS_KEYWORD(self, token: Token) -> Location:  # noqa: N802
        return FileLocation._from_token(token)

    def goals_section(
        self, location: Location, goals: list[Condition[Object]]
    ) -> GoalList:
        return GoalList(goals, location=location)

    def problem(
        self,
        name: Identifier,
        used_domain_name: Identifier,
        requirements: RequirementSet,
        objects: list[Typed[Object]] | None,
        fallible_actions: ActionFallibilitySet | None,
        revealables: RevealableSet | None,
        initialization: list[Predicate[Object]] | None,
        goal_conditions: GoalList | Condition[Object],
    ) -> RawProblem:
        return RawProblem.from_raw_parts(
            name,
            used_domain_name,
            requirements,
            objects if objects else [],
            fallible_actions,
            revealables,
            initialization if initialization else [],
            goal_conditions,
        )


# Cache the parser for each invocation, and persist it
_PDDL_PARSER = Lark(
    _RESOURCES.joinpath("grammar.lark").read_text(),
    parser="lalr",
    cache=True,
    transformer=_PDDLTransformer(),
    start=["domain", "problem"],
)


def parse_domain(text: str) -> Domain:
    """Construct a `pddlsim.ast.Domain` from PDDL text."""
    return cast(Domain, _PDDL_PARSER.parse(text, "domain"))


def parse_problem(text: str, domain: Domain) -> Problem:
    """Construct a `pddlsim.ast.Problem` from PDDL text.

    Due to validation concerns, this function requires an existing
    `pddlsim.ast.Domain` object, corresponding to the domain used
    in the problem.
    """
    return Problem(
        cast(
            RawProblem,
            _PDDL_PARSER.parse(text, "problem"),
        ),
        domain,
    )


def parse_domain_problem_pair(
    domain_text: str, problem_text: str
) -> tuple[Domain, Problem]:
    """Construct a `pddlsim.ast.Domain` and a `pddlsim.ast.Problem` from text.

    This is a convenience function to avoid manually passing a
    `pddlsim.ast.Domain` into `parse_problem`.
    """
    domain = parse_domain(domain_text)
    problem = parse_problem(problem_text, domain)

    return (domain, problem)


def parse_domain_from_file(path: str | os.PathLike) -> Domain:
    """Construct a `pddlsim.ast.Domain` from the path to a file.

    This is a convenience function to avoid manual I/O.
    """
    with open(path) as file:
        return parse_domain(file.read())


def parse_problem_from_file(path: str | os.PathLike, domain: Domain) -> Problem:
    """Construct a `pddlsim.ast.Problem` from the path to a file.

    This is a convenience function to avoid manual I/O. Like `parse_problem`, it
    requires manually passing the `pddlsim.ast.Domain` object corresponding to
    the domain used in the problem, for validation of the problem.
    """
    with open(path) as file:
        return parse_problem(file.read(), domain)


def parse_domain_problem_pair_from_files(
    domain_path: str | os.PathLike, problem_path: str | os.PathLike
) -> tuple[Domain, Problem]:
    """Construct a `pddlsim.ast.Domain` and a `pddlsim.ast.Problem` from paths.

    This is a convenience function to avoid manual I/O. Like
    `parse_domain_problem_pair`, it mainly exists to avoid passing a
    `pddlsim.ast.Domain` manually into `parse_problem_from_file`.
    """
    domain = parse_domain_from_file(domain_path)
    problem = parse_problem_from_file(problem_path, domain)

    return (domain, problem)
