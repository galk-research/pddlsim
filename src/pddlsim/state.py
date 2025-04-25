from collections.abc import Iterable, MutableSet
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


@dataclass
class SimulationState:
    """
    Stores a state of the simulation, which is based on classical PDDL.
    Therefore, a state is a set of true predicates.
    """

    _true_predicates: MutableSet[Predicate[Object]] = field(default_factory=set)

    def does_atom_hold(self, atom: Atom[Object]) -> bool:
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
                self._true_predicates.remove(base_predicate.value)

    def does_condition_hold(self, condition: Condition[Object]) -> bool:
        match condition:
            case AndCondition(subconditions):
                return all(
                    self.does_condition_hold(subcondition.value)
                    for subcondition in subconditions
                )
            case OrCondition(subconditions):
                return any(
                    self.does_condition_hold(subcondition.value)
                    for subcondition in subconditions
                )
            case NotCondition(base_condition):
                return not (self.does_condition_hold(base_condition.value))
            case EqualityCondition(left_side, right_side):
                return left_side == right_side
            case Predicate():
                return self.does_atom_hold(condition)

    def _make_effect_hold(self, effect: Effect[Object], rng: Random) -> None:
        match effect:
            case AndEffect(subeffects):
                for subeffect in subeffects:
                    self._make_effect_hold(subeffect.value, rng)
            case ProbabilisticEffect():
                self._make_effect_hold(
                    effect.choose_possibility(rng).value, rng
                )
            case Predicate() | NotPredicate():
                self._make_atom_hold(effect)

    def true_predicates(self) -> Iterable[Predicate[Object]]:
        return iter(self._true_predicates)
