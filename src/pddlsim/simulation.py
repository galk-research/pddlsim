import itertools
import os
from collections import defaultdict
from collections.abc import (
    Generator,
    Iterable,
    Mapping,
)
from dataclasses import dataclass
from functools import cached_property
from random import Random
from typing import TypedDict, cast

from clingo import Control
from koda_validate import TypedDictValidator, Validator

from pddlsim._asp import (
    ASPPart,
    ASPPartKind,
    IDAllocator,
    ObjectNameID,
    PredicateID,
    TypeNameID,
    VariableID,
    action_definition_asp_part,
    objects_asp_part,
    simulation_state_asp_part,
)
from pddlsim._serde import Serdeable
from pddlsim.ast import (
    ActionDefinition,
    ActionFallibility,
    AndCondition,
    AndEffect,
    Argument,
    Condition,
    Domain,
    Effect,
    EqualityCondition,
    Identifier,
    NotCondition,
    NotPredicate,
    Object,
    OrCondition,
    Predicate,
    ProbabilisticEffect,
    Problem,
    Revealable,
    Type,
    Variable,
)
from pddlsim.state import SimulationState


def _ground_argument(
    argument: Argument, grounding: Mapping[Variable, Object]
) -> Object:
    return grounding[argument] if isinstance(argument, Variable) else argument


def _ground_predicate(
    predicate: Predicate[Argument], grounding: Mapping[Variable, Object]
) -> Predicate[Object]:
    return Predicate(
        predicate.name,
        tuple(
            _ground_argument(argument, grounding)
            for argument in predicate.assignment
        ),
    )


def _ground_condition(
    condition: Condition[Argument], grounding: Mapping[Variable, Object]
) -> Condition[Object]:
    match condition:
        case AndCondition(subconditions):
            return AndCondition(
                [
                    _ground_condition(subcondition, grounding)
                    for subcondition in subconditions
                ]
            )
        case OrCondition(subconditions):
            return OrCondition(
                [
                    _ground_condition(subcondition, grounding)
                    for subcondition in subconditions
                ]
            )
        case NotCondition(base_condition):
            return NotCondition(_ground_condition(base_condition, grounding))
        case EqualityCondition(left_side, right_side):
            return EqualityCondition(
                _ground_argument(left_side, grounding),
                _ground_argument(right_side, grounding),
            )
        case Predicate():
            return _ground_predicate(condition, grounding)


def _ground_effect(
    effect: Effect[Argument], grounding: Mapping[Variable, Object]
) -> Effect[Object]:
    match effect:
        case AndEffect(subeffects):
            return AndEffect(
                [
                    _ground_effect(subeffect, grounding)
                    for subeffect in subeffects
                ]
            )
        case ProbabilisticEffect():
            return ProbabilisticEffect(
                [
                    _ground_effect(possible_effect, grounding)
                    for possible_effect in effect._possible_effects
                ],
                effect._cummulative_probabilities,
            )
        case Predicate():
            return _ground_predicate(effect, grounding)
        case NotPredicate(base_predicate):
            return NotPredicate(
                cast(
                    Predicate[Object],
                    _ground_effect(base_predicate, grounding),
                )
            )


class _ActionGroundingPair(TypedDict):
    name: str
    grounding: list[str]


@dataclass(frozen=True)
class GroundedAction(Serdeable[_ActionGroundingPair]):
    name: Identifier
    grounding: list[Object]

    def serialize(self) -> _ActionGroundingPair:
        return _ActionGroundingPair(
            name=self.name.value,
            grounding=[object_.value for object_ in self.grounding],
        )

    @classmethod
    def validator(cls) -> Validator[_ActionGroundingPair]:
        return TypedDictValidator(_ActionGroundingPair)

    @classmethod
    def create(cls, value: _ActionGroundingPair) -> "GroundedAction":
        return GroundedAction(
            Identifier(value["name"]),
            [Object(object_) for object_ in value["grounding"]],
        )


class SimulationCompletedError(Exception):
    pass


@dataclass(frozen=True)
class Simulation:
    domain: Domain
    problem: Problem

    _rng: Random

    _state: SimulationState
    _reached_goal_indices: set[int]
    _unreached_goal_indices: set[int]

    _unactivated_revealables: set[Revealable]

    @cached_property
    def _object_name_id_allocator(self) -> IDAllocator[Object]:
        return IDAllocator(ObjectNameID)

    @cached_property
    def _predicate_id_allocator(self) -> IDAllocator[Identifier]:
        return IDAllocator(PredicateID)

    @cached_property
    def _type_name_id_allocator(self) -> IDAllocator[Type]:
        return IDAllocator(TypeNameID)

    @cached_property
    def _action_fallibilities(
        self,
    ) -> Mapping[Identifier, Iterable[ActionFallibility]]:
        fallibilities = defaultdict(list)

        for fallibility in self.problem.action_fallibilities:
            fallibilities[fallibility.action_name].append(fallibility)

        return fallibilities

    @cached_property
    def _objects_asp_part(self) -> ASPPart:
        return objects_asp_part(
            self.domain,
            self.problem,
            self._object_name_id_allocator,
            self._type_name_id_allocator,
        )

    @cached_property
    def _action_definition_asp_parts(
        self,
    ) -> Mapping[Identifier, tuple[ASPPart, IDAllocator[Variable]]]:
        return {
            action_definition.name: (
                action_definition_asp_part(
                    action_definition,
                    variable_id_allocator := IDAllocator[Variable](VariableID),
                    self._object_name_id_allocator,
                    self._predicate_id_allocator,
                    self._type_name_id_allocator,
                ),
                variable_id_allocator,
            )
            for action_definition in self.domain.action_definitions.values()
        }

    @classmethod
    def from_domain_and_problem(
        cls,
        domain: Domain,
        problem: Problem,
        state_override: SimulationState | None = None,
        reached_goal_indices_override: Iterable[int] | None = None,
        seed: int | float | str | bytes | bytearray | None = None,
    ) -> "Simulation":
        reached_goal_indices = (
            set(reached_goal_indices_override)
            if reached_goal_indices_override
            else set()
        )

        return Simulation(
            domain,
            problem,
            # Technically speaking, the seed could be cracked under very
            # specific circumstances (system time is known and is used
            # for randomness), but in practice, this is fine, and shouldn't
            # be exploited.
            Random(seed),
            # Internally, we mutate the state, so copying is needed
            state_override._copy()
            if state_override
            else SimulationState(
                {true_predicate for true_predicate in problem.initialization}
            ),
            reached_goal_indices,
            set(range(len(problem.goal_conditions))) - reached_goal_indices,
            set(problem.revealables),
        )

    def __post_init__(self) -> None:
        self._update_reached_goals()
        self._update_revealables()

    def _update_reached_goals(self) -> None:
        newly_reached_goals = set()

        for goal_index in self._unreached_goal_indices:
            if self.state.does_condition_hold(
                self.problem.goal_conditions[goal_index]
            ):
                self._reached_goal_indices.add(goal_index)
                newly_reached_goals.add(goal_index)

        self._unreached_goal_indices.difference_update(newly_reached_goals)

    def _update_revealables(self) -> None:
        newly_active_revealables = set()

        while True:
            for revealable in self._unactivated_revealables:
                if self.state.does_condition_hold(revealable.condition):
                    should_reveal = (
                        self._rng.random() < revealable.with_probability
                    )

                    if should_reveal:
                        self.state._make_effect_hold(
                            revealable.effect, self._rng
                        )
                        newly_active_revealables.add(revealable)

            if newly_active_revealables:
                self._unactivated_revealables.difference_update(
                    newly_active_revealables
                )

                newly_active_revealables.clear()
            else:
                break

    @property
    def state(self) -> SimulationState:
        return self._state

    @property
    def reached_goal_indices(self) -> list[int]:
        return list(self._reached_goal_indices)

    @property
    def unreached_goal_indices(self) -> list[int]:
        return list(self._unreached_goal_indices)

    def apply_grounded_action(self, grounded_action: GroundedAction) -> None:
        if self.is_solved():
            raise SimulationCompletedError

        for fallibility in self._action_fallibilities[grounded_action.name]:
            if self.state.does_condition_hold(fallibility.condition):
                does_fail = self._rng.random() < fallibility.with_probability

                if does_fail:
                    return

        action_definition = self.domain.action_definitions[grounded_action.name]
        grounding = {
            variable: object_
            for variable, object_ in zip(
                action_definition.variable_types,
                grounded_action.grounding,
                strict=True,
            )
        }

        if self.state.does_condition_hold(
            _ground_condition(action_definition.precondition, grounding)
        ):
            self.state._make_effect_hold(
                _ground_effect(action_definition.effect, grounding),
                self._rng,
            )

            self._update_reached_goals()
            self._update_revealables()
        else:
            raise ValueError("grounded action doesn't satisfy precondition")

    def _get_groundings(
        self, action_definition: ActionDefinition, state_part: ASPPart
    ) -> Generator[Mapping[Variable, Object]]:
        action_definition_asp_part, variable_id_allocator = (
            self._action_definition_asp_parts[action_definition.name]
        )

        # `-Wno-atom-undefined` disables warnings about undefined atoms
        # from Clingo. This is useful, as for some simulation states,
        # a predicate has no valid assignments, and won't show up
        # in the ASP program.
        control = Control(["-Wno-atom-undefined"])

        # Set number of threads to use
        control.configuration.solve.parallel_mode = os.cpu_count()  # type: ignore
        # Compute all models (all groundings)
        control.configuration.solve.models = 0  # type: ignore

        self._objects_asp_part.add_to_control(control)
        state_part.add_to_control(control)
        action_definition_asp_part.add_to_control(control)

        control.ground(
            (
                (ASPPartKind.OBJECTS, ()),
                (ASPPartKind.STATE, ()),
                (ASPPartKind.ACTION_DEFINITION, ()),
            )
        )

        with control.solve(yield_=True) as handle:
            for model in handle:
                yield {
                    variable_id_allocator.get_value(
                        VariableID.from_str(symbol.name)
                    ): self._object_name_id_allocator.get_value(
                        ObjectNameID.from_str(symbol.arguments[0].name)
                    )
                    for symbol in model.symbols(shown=True)
                }

    def _get_grounded_actions(
        self, action_definition: ActionDefinition, state_part: ASPPart
    ) -> Iterable[GroundedAction]:
        return (
            GroundedAction(
                action_definition.name,
                [
                    grounding[variable]
                    for variable in action_definition.variable_types
                ],
            )
            for grounding in self._get_groundings(action_definition, state_part)
        )

    def get_grounded_actions(self) -> Iterable[GroundedAction]:
        state_part = simulation_state_asp_part(
            self.state,
            self._predicate_id_allocator,
            self._object_name_id_allocator,
        )

        return (
            grounded_action
            for action_definition in self.domain.action_definitions.values()
            for grounded_action in self._get_grounded_actions(
                action_definition, state_part
            )
        )

    def is_solved(self) -> bool:
        return len(self._reached_goal_indices) == len(
            self.problem.goal_conditions
        )
