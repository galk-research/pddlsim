import importlib.resources
from dataclasses import dataclass
from importlib.abc import Traversable

import pytest

from pddlsim.agents.previous_state_avoider import PreviousStateAvoider
from pddlsim.ast import Domain, Problem
from pddlsim.local import simulate_configuration
from pddlsim.parser import (
    parse_domain_problem_pair,
)
from pddlsim.remote.server import SimulatorConfiguration
from tests import preprocess_traversables

RESOURCES = importlib.resources.files(__name__)


@dataclass
class LocalSimulationCase:
    domain: Domain
    problem: Problem


def _preprocess_gga_case(traversable: Traversable) -> LocalSimulationCase:
    domain_text = traversable.joinpath("domain.pddl").read_text()
    problem_text = traversable.joinpath("problem.pddl").read_text()

    domain, problem = parse_domain_problem_pair(domain_text, problem_text)

    return LocalSimulationCase(domain, problem)


CASES = preprocess_traversables(
    RESOURCES.joinpath("cases"), _preprocess_gga_case
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case",
    CASES.values(),
    ids=CASES.keys(),
)
async def test_gga(case: LocalSimulationCase) -> None:
    await simulate_configuration(
        SimulatorConfiguration(case.domain, case.problem),
        PreviousStateAvoider.configure(),
    )
