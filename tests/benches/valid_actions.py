import random

from pytest_benchmark.fixture import BenchmarkFixture

from pddlsim.executors.random_executor import RandomExecutor
from pddlsim.local_simulator import LocalSimulator

random.seed(42)


# TODO: Simulate for a fixed number of actions
def random_executor_run(domain_path, problem_path):
    executor = RandomExecutor()
    LocalSimulator().run(
        domain_path,
        problem_path,
        executor,
    )


def test_maze_5_5_5_valid_actions(benchmark: BenchmarkFixture):
    benchmark(
        random_executor_run,
        "domains/generated/domain.pddl",
        "domains/generated/problems/t_5_5_5.pddl",
    )


def test_maze_10_10_10_valid_actions(benchmark: BenchmarkFixture):
    benchmark(
        random_executor_run,
        "domains/generated/domain.pddl",
        "domains/generated/problems/t_10_10_10.pddl",
    )


def test_maze_50_5_5_valid_actions(benchmark: BenchmarkFixture):
    benchmark(
        random_executor_run,
        "domains/generated/domain.pddl",
        "domains/generated/problems/t_10_10_10.pddl",
    )
