import os
from collections.abc import (
    Generator,
    Iterable,
    Mapping,
)
from dataclasses import dataclass
from random import Random
from typing import TypedDict, cast

from clingo import Control
from koda_validate import TypedDictValidator, Validator

from pddlsim._serde import Serdeable
from pddlsim.asp import (
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
from pddlsim.ast import (
    ActionDefinition,
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


class ActionGroundingPair(TypedDict):
    name: str
    grounding: list[str]


@dataclass(frozen=True)
class GroundedAction(Serdeable[ActionGroundingPair]):
    name: Identifier
    grounding: list[Object]

    def serialize(self) -> ActionGroundingPair:
        return ActionGroundingPair(
            name=self.name.value,
            grounding=[object_.value for object_ in self.grounding],
        )

    @classmethod
    def validator(cls) -> Validator[ActionGroundingPair]:
        return TypedDictValidator(ActionGroundingPair)

    @classmethod
    def create(cls, value: ActionGroundingPair) -> "GroundedAction":
        return GroundedAction(
            Identifier(value["name"]),
            [Object(object_) for object_ in value["grounding"]],
        )


class SimulationCompletedError(Exception):
    pass


@dataclass
class Simulation:
    _domain: Domain
    _problem: Problem

    _rng: Random
    _state: SimulationState

    _object_name_id_allocator: IDAllocator[Object]
    _predicate_id_allocator: IDAllocator[Identifier]
    _type_name_id_allocator: IDAllocator[Type]

    _objects_asp_part: ASPPart
    _action_definition_asp_parts: Mapping[
        Identifier, tuple[ASPPart, IDAllocator[Variable]]
    ]

    @classmethod
    def from_domain_and_problem(
        cls, domain: Domain, problem: Problem, seed: int = 42
    ) -> "Simulation":
        object_name_id_allocator = IDAllocator[Object](ObjectNameID)
        predicate_id_allocator = IDAllocator[Identifier](PredicateID)
        type_name_id_allocator = IDAllocator[Type](TypeNameID)

        return Simulation(
            domain,
            problem,
            Random(seed),
            SimulationState(
                {true_predicate for true_predicate in problem.initialization}
            ),
            object_name_id_allocator,
            predicate_id_allocator,
            type_name_id_allocator,
            objects_asp_part(
                domain,
                problem,
                object_name_id_allocator,
                type_name_id_allocator,
            ),
            {
                action_definition.name: (
                    action_definition_asp_part(
                        action_definition,
                        variable_id_allocator := IDAllocator[Variable](
                            VariableID
                        ),
                        object_name_id_allocator,
                        predicate_id_allocator,
                        type_name_id_allocator,
                    ),
                    variable_id_allocator,
                )
                for action_definition in domain.action_definitions.values()
            },
        )

    @property
    def domain(self) -> Domain:
        return self._domain

    @property
    def problem(self) -> Problem:
        return self._problem

    @property
    def state(self) -> SimulationState:
        return self._state

    def apply_grounded_action(self, grounded_action: GroundedAction) -> None:
        if self.is_solved():
            raise SimulationCompletedError

        action_definition = self._domain.action_definitions[
            grounded_action.name
        ]
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
            self._state,
            self._predicate_id_allocator,
            self._object_name_id_allocator,
        )

        return (
            grounded_action
            for action_definition in self._domain.action_definitions.values()
            for grounded_action in self._get_grounded_actions(
                action_definition, state_part
            )
        )

    def is_solved(self) -> bool:
        return self.state.does_condition_hold(self._problem.goal_condition)
