from pytest_benchmark.fixture import BenchmarkFixture

from pddlsim.fd_parser import FDParser
from pddlsim.services.perception import Perception
from pddlsim.services.valid_actions import ValidActions


def benchmark_and_test_valid_actions(
    benchmark: BenchmarkFixture,
    domain_path: str,
    problem_path: str,
    actions: list[str],
    expected_valid_actions: set[str],
):
    parser = FDParser(
        domain_path,
        problem_path,
    )

    state = parser.copy_state(parser.initial_state)

    for action in actions:
        parser.apply_action_to_state(action, state)

    assert expected_valid_actions == set(
        benchmark(lambda: ValidActions(parser, Perception(lambda: state)).get())
    )


def test_maze_5_5_5_valid_actions(benchmark: BenchmarkFixture):
    benchmark_and_test_valid_actions(
        benchmark,
        "domains/generated/domain.pddl",
        "domains/generated/problems/t_5_5_5.pddl",
        [
            "(move-east person1 start_tile c0)",
            "(move-east person1 c0 c1)",
            "(move-east person1 c1 c2)",
            "(move-east person1 c2 c3)",
            "(move-south person1 c3 d0)",
        ],
        {"(move-south person1 d0 d1)", "(move-north person1 d0 c3)"},
    )
