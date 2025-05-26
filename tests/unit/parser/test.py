import importlib.resources
from dataclasses import dataclass
from importlib.abc import Traversable

import pytest
from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore

from pddlsim.ast import Domain, Problem
from pddlsim.parser import (
    parse_domain_problem_pair,
)
from tests import preprocess_traversables

RESOURCES = importlib.resources.files(__name__)


@dataclass
class ParserCase:
    domain: Domain
    problem: Problem


def _preprocess_gga_case(traversable: Traversable) -> ParserCase:
    domain_text = traversable.joinpath("domain.pddl").read_text()
    problem_text = traversable.joinpath("problem.pddl").read_text()

    domain, problem = parse_domain_problem_pair(domain_text, problem_text)

    return ParserCase(domain, problem)


CASES = preprocess_traversables(
    RESOURCES.joinpath("cases"), _preprocess_gga_case
)


@pytest.mark.parametrize(
    "case",
    CASES.values(),
    ids=CASES.keys(),
)
def test_parser_roundtrip(
    benchmark: BenchmarkFixture, case: ParserCase
) -> None:
    def roundtrip() -> tuple[Domain, Problem]:
        domain_text = case.domain.as_pddl()
        problem_text = case.problem.as_pddl()

        return parse_domain_problem_pair(domain_text, problem_text)

    domain, problem = benchmark(roundtrip)

    assert domain == case.domain
    assert problem == case.problem
