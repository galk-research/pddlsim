import importlib.resources
from collections.abc import Set
from dataclasses import dataclass
from importlib.abc import Traversable

import pytest
from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore

from pddlsim.ast import Domain, GroundedAction, Identifier, Object, Problem
from pddlsim.parser import (
    parse_domain_problem_pair,
)
from pddlsim.simulation import Simulation
from tests import preprocess_traversables

RESOURCES = importlib.resources.files(__name__)


@dataclass
class GGACase:
    domain: Domain
    problem: Problem
    expected_grounded_actions: Set[GroundedAction]

    def assert_match(self, found_grounded_actions: Set[GroundedAction]) -> None:
        assert self.expected_grounded_actions == found_grounded_actions


def _grounded_action_from_text(text: str) -> GroundedAction:
    text_without_parentheses = text[1:-1]
    elements = text_without_parentheses.split(" ")

    action_name = elements[0]
    grounding = elements[1:]

    return GroundedAction(
        Identifier(action_name), tuple(Object(object_) for object_ in grounding)
    )


def _preprocess_gga_case(traversable: Traversable) -> GGACase:
    domain_text = traversable.joinpath("domain.pddl").read_text()
    problem_text = traversable.joinpath("problem.pddl").read_text()

    domain, problem = parse_domain_problem_pair(domain_text, problem_text)

    expected_grounded_actions = set(
        _grounded_action_from_text(line)
        for line in traversable.joinpath("output.txt").read_text().splitlines()
    )

    return GGACase(domain, problem, expected_grounded_actions)


CASES = preprocess_traversables(
    RESOURCES.joinpath("cases"), _preprocess_gga_case
)


@pytest.mark.parametrize(
    "case",
    CASES.values(),
    ids=CASES.keys(),
)
def test_gga(benchmark: BenchmarkFixture, case: GGACase) -> None:
    grounded_actions = benchmark(
        lambda: set(
            Simulation.from_domain_and_problem(
                case.domain, case.problem
            ).get_grounded_actions()
        )
    )

    case.assert_match(grounded_actions)
