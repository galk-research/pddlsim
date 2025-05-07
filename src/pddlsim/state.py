from collections.abc import Iterable, Iterator, MutableSet
from dataclasses import dataclass, field
from random import Random

from pddlsim.ast import (
    AndCondition,
    AndEffect,
    Atom,
    Condition,
    Effect,
    EqualityCondition,
    NotCondition,
    NotPredicate,
    Object,
    OrCondition,
    Predicate,
    ProbabilisticEffect,
)


@dataclass(eq=True, frozen=True)
class SimulationState:
    _true_predicates: MutableSet[Predicate[Object]] = field(default_factory=set)

    def _copy(self) -> "SimulationState":
        return SimulationState(set(self._true_predicates))

    def _does_atom_hold(self, atom: Atom[Object]) -> bool:
        match atom:
            case Predicate():
                return atom in self._true_predicates
            case NotPredicate(base_predicate):
                return base_predicate not in self._true_predicates

    def _make_atom_hold(self, atom: Atom[Object]) -> None:
        match atom:
            case Predicate():
                self._true_predicates.add(atom)
            case NotPredicate(base_predicate):
                self._true_predicates.remove(base_predicate)

    def does_condition_hold(self, condition: Condition[Object]) -> bool:
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
                return self._does_atom_hold(condition)

    def _make_effect_hold(self, effect: Effect[Object], rng: Random) -> None:
        match effect:
            case AndEffect(subeffects):
                for subeffect in subeffects:
                    self._make_effect_hold(subeffect, rng)
            case ProbabilisticEffect():
                self._make_effect_hold(effect.choose_possibility(rng), rng)
            case Predicate() | NotPredicate():
                self._make_atom_hold(effect)

    def make_effect_hold(
        self, effect: Effect[Object], rng: Random
    ) -> "SimulationState":
        new_state = self._copy()

        new_state._make_effect_hold(effect, rng)

        return new_state

    def __iter__(self) -> Iterator[Predicate[Object]]:
        return iter(self._true_predicates)
