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


def test_rovers_problem_17_valid_actions(benchmark: BenchmarkFixture):
    benchmark_and_test_valid_actions(
        benchmark,
        "domains/ipc2002/rovers/domain.pddl",
        "domains/ipc2002/rovers/prob17.pddl",
        [
            "(calibrate rover5 camera6 objective6 waypoint0)",
            "(take_image rover5 waypoint0 objective3 camera6 low_res)",
            "(calibrate rover5 camera6 objective6 waypoint0)",
            "(take_image rover5 waypoint0 objective4 camera6 high_res)",
            "(communicate_image_data rover5 general objective4 high_res waypoint0 waypoint17)",
        ],
        {
            "(calibrate rover0 camera5 objective2 waypoint2)",
            "(calibrate rover1 camera0 objective4 waypoint9)",
            "(calibrate rover2 camera1 objective6 waypoint0)",
            "(calibrate rover4 camera2 objective0 waypoint3)",
            "(calibrate rover5 camera6 objective6 waypoint0)",
            "(communicate_image_data rover5 general objective3 low_res waypoint0 waypoint17)",
            "(communicate_image_data rover5 general objective4 high_res waypoint0 waypoint17)",
            "(navigate rover0 waypoint2 waypoint0)",
            "(navigate rover0 waypoint2 waypoint14)",
            "(navigate rover0 waypoint2 waypoint18)",
            "(navigate rover0 waypoint2 waypoint6)",
            "(navigate rover0 waypoint2 waypoint7)",
            "(navigate rover0 waypoint2 waypoint9)",
            "(navigate rover1 waypoint9 waypoint0)",
            "(navigate rover1 waypoint9 waypoint10)",
            "(navigate rover1 waypoint9 waypoint12)",
            "(navigate rover1 waypoint9 waypoint14)",
            "(navigate rover1 waypoint9 waypoint18)",
            "(navigate rover1 waypoint9 waypoint19)",
            "(navigate rover1 waypoint9 waypoint3)",
            "(navigate rover1 waypoint9 waypoint4)",
            "(navigate rover1 waypoint9 waypoint7)",
            "(navigate rover2 waypoint0 waypoint1)",
            "(navigate rover2 waypoint0 waypoint13)",
            "(navigate rover2 waypoint0 waypoint16)",
            "(navigate rover2 waypoint0 waypoint17)",
            "(navigate rover2 waypoint0 waypoint18)",
            "(navigate rover2 waypoint0 waypoint9)",
            "(navigate rover3 waypoint18 waypoint0)",
            "(navigate rover3 waypoint18 waypoint11)",
            "(navigate rover3 waypoint18 waypoint4)",
            "(navigate rover4 waypoint3 waypoint10)",
            "(navigate rover4 waypoint3 waypoint11)",
            "(navigate rover4 waypoint3 waypoint13)",
            "(navigate rover4 waypoint3 waypoint15)",
            "(navigate rover4 waypoint3 waypoint6)",
            "(navigate rover4 waypoint3 waypoint7)",
            "(navigate rover4 waypoint3 waypoint9)",
            "(navigate rover5 waypoint0 waypoint1)",
            "(navigate rover5 waypoint0 waypoint12)",
            "(navigate rover5 waypoint0 waypoint13)",
            "(navigate rover5 waypoint0 waypoint17)",
            "(navigate rover5 waypoint0 waypoint18)",
            "(sample_rock rover0 rover0store waypoint2)",
            "(sample_rock rover1 rover1store waypoint9)",
            "(sample_rock rover3 rover3store waypoint18)",
            "(sample_soil rover2 rover2store waypoint0)",
            "(sample_soil rover4 rover4store waypoint3)",
        },
    )
