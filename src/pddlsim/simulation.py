import os
from collections import defaultdict
from collections.abc import (
    Generator,
    Iterable,
    Mapping,
    MutableMapping,
    MutableSet,
)
from dataclasses import dataclass
from random import Random

from clingo import Control

from pddlsim.asp import ID, IDAllocator, IDKind
from pddlsim.parser import (
    ActionDefinition,
    AndCondition,
    AndEffect,
    Argument,
    Atom,
    Condition,
    Domain,
    Effect,
    EqualityCondition,
    Identifier,
    NotCondition,
    NotPredicate,
    ObjectName,
    OrCondition,
    Predicate,
    ProbabilisticEffect,
    Problem,
    TypeName,
    Variable,
)


def _ground_argument(
    argument: Argument, grounding: Mapping[Variable, ObjectName]
) -> ObjectName:
    return grounding[argument] if isinstance(argument, Variable) else argument


def _ground_predicate(
    predicate: Predicate[Argument], grounding: Mapping[Variable, ObjectName]
) -> Predicate[ObjectName]:
    return Predicate(
        predicate.name,
        [
            _ground_argument(argument, grounding)
            for argument in predicate.assignment
        ],
    )


def _ground_condition(
    condition: Condition[Argument], grounding: Mapping[Variable, ObjectName]
) -> Condition[ObjectName]:
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
    effect: Effect[Argument], grounding: Mapping[Variable, ObjectName]
) -> Effect[ObjectName]:
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
            return _ground_effect(base_predicate, grounding)


class SimulationState:
    """
    Stores a state of the simulation, which is based on classical PDDL.
    Therefore, a state is a set of true predicates.
    """

    _true_predicates: MutableSet[Predicate[ObjectName]] = set()

    def does_atom_hold(self, atom: Atom[ObjectName]) -> bool:
        match atom:
            case Predicate():
                return atom in self._true_predicates
            case NotPredicate(base_predicate):
                return base_predicate not in self._true_predicates

    def _make_atom_hold(self, atom: Atom[ObjectName]) -> None:
        match atom:
            case Predicate():
                self._true_predicates.add(atom)
            case NotPredicate(base_predicate):
                self._true_predicates.remove(base_predicate)

    def does_condition_hold(self, condition: Condition[ObjectName]) -> bool:
        match condition:
            case AndCondition(subconditions):
                return all(
                    self.does_condition_hold(subcondition)
                    for subcondition in subconditions
                )
            case OrCondition(subconditions):
                return any(
                    self.does_condition_hold(subcondition)
                    for subcondition in subconditions
                )
            case NotCondition(base_condition):
                return not (self.does_condition_hold(base_condition))
            case EqualityCondition(left_side, right_side):
                return left_side == right_side
            case Predicate():
                return self.does_atom_hold(condition)

    def _make_effect_hold(
        self, effect: Effect[ObjectName], rng: Random
    ) -> None:
        match effect:
            case AndEffect(subeffects):
                for subeffect in subeffects:
                    self._make_effect_hold(subeffect, rng)
            case ProbabilisticEffect():
                self._make_effect_hold(effect.choose_possibility(rng), rng)
            case Predicate() | NotPredicate():
                self._make_atom_hold(effect)

    def percepts(self) -> dict[str, list[list[str]]]:
        percepts = defaultdict(list)

        for predicate in self._true_predicates:
            percepts[predicate.name.value].append(
                [object_name.value for object_name in predicate.assignment]
            )

        return percepts

    def _as_asp_part(
        self,
        predicate_id_allocator: IDAllocator[Identifier],
        object_name_id_allocator: IDAllocator[ObjectName],
    ) -> str:
        result = []

        for predicate in self._true_predicates:
            arguments = (
                str(object_name_id_allocator.get_id_or_insert(object_name))
                for object_name in predicate.assignment
            )
            predicate_id = predicate_id_allocator.get_id_or_insert(
                predicate.name
            )

            result.append(f"{predicate_id}({', '.join(arguments)}).")

        return "\n".join(result)


@dataclass(eq=True, frozen=True)
class GroundedAction:
    name: Identifier
    grounding: tuple[ObjectName, ...]


class SimulationCompletedError(Exception):
    pass


class Simulation:
    def __init__(
        self, domain: Domain, problem: Problem, seed: int = 42
    ) -> None:
        self._domain = domain
        self._problem = problem
        self._rng = Random(seed)
        self._state = SimulationState()
        self._action_definition_asp_parts: MutableMapping[
            Identifier, tuple[str, IDAllocator[Variable]]
        ] = {}
        self._object_name_id_allocator = IDAllocator[ObjectName](
            IDKind.OBJECT_NAME
        )
        self._predicate_id_allocator = IDAllocator[Identifier](IDKind.PREDICATE)
        self._type_name_id_allocator = IDAllocator[TypeName](IDKind.TYPE_NAME)
        self._objects_asp_part = ""

        self._initialize_state()
        self._initialize_action_definition_asp_parts()
        self._initialize_objects_asp_part()

    def _initialize_state(self) -> None:
        for predicate in self._problem.initialization:
            self._state._make_atom_hold(predicate)

    def _initialize_action_definition_asp_parts(self) -> None:
        for action_definition in self._domain.action_definitions.values():
            variable_id_allocator = IDAllocator[Variable](IDKind.VARIABLE)

            self._action_definition_asp_parts[action_definition.name] = (
                action_definition._as_asp_program(
                    variable_id_allocator,
                    self._object_name_id_allocator,
                    self._predicate_id_allocator,
                    self._type_name_id_allocator,
                ),
                variable_id_allocator,
            )

    def _initialize_objects_asp_part(self) -> None:
        result = []

        for typed_object in self._problem.objects:
            type_name_id = self._type_name_id_allocator.get_id_or_insert(
                typed_object.type_name
            )
            object_name_id = self._object_name_id_allocator.get_id_or_insert(
                typed_object.value
            )

            result.append(f"{type_name_id}({object_name_id}).")

        for member in self._domain.type_hierarchy:
            custom_type = member.value
            supertype = member.type_name

            custom_type_id = self._type_name_id_allocator.get_id_or_insert(
                custom_type
            )
            supertype_id = self._type_name_id_allocator.get_id_or_insert(
                supertype
            )

            result.append(f"{supertype_id}(O) :- {custom_type_id}(O).")

        self._objects_asp_part = "\n".join(result)

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
            parameter.value: object_name
            for parameter, object_name in zip(
                action_definition.parameters,
                grounded_action.grounding,
                strict=True,
            )
        }

        if self.state.does_condition_hold(
            _ground_condition(action_definition.precondition, grounding)
        ):
            self.state._make_effect_hold(
                _ground_effect(action_definition.effect, grounding), self._rng
            )
        else:
            raise ValueError("grounded action doesn't satisfy precondition")

    def _get_groundings(
        self, action_definition: ActionDefinition, state_asp_part: str
    ) -> Generator[Mapping[Variable, ObjectName]]:
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

        control.add("objects", (), self._objects_asp_part)
        control.add("state", (), state_asp_part)
        control.add("precondition", (), action_definition_asp_part)

        control.ground((("objects", ()), ("state", ()), ("precondition", ())))

        with control.solve(yield_=True) as handle:
            for model in handle:
                yield {
                    variable_id_allocator.get_value(
                        ID.from_str(symbol.name)
                    ): self._object_name_id_allocator.get_value(
                        ID.from_str(symbol.arguments[0].name)
                    )
                    for symbol in model.symbols(shown=True)
                }

    def _get_grounded_actions(
        self, action_definition: ActionDefinition, state_asp_part: str
    ) -> Iterable[GroundedAction]:
        return (
            GroundedAction(
                action_definition.name,
                tuple(
                    grounding[parameter.value]
                    for parameter in action_definition.parameters
                ),
            )
            for grounding in self._get_groundings(
                action_definition, state_asp_part
            )
        )

    def get_grounded_actions(self) -> Iterable[GroundedAction]:
        asp_program_facts = self.state._as_asp_part(
            self._predicate_id_allocator, self._object_name_id_allocator
        )

        return (
            grounded_action
            for action_definition in self._domain.action_definitions.values()
            for grounded_action in self._get_grounded_actions(
                action_definition, asp_program_facts
            )
        )

    def is_solved(self) -> bool:
        return self.state.does_condition_hold(self._problem.goal_condition)
