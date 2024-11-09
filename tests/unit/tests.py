from pddlsim.fd_parser import FDParser
from pddlsim.local_simulator import LocalSimulator

from pddlsim.executor import Executor
import random
from pddlsim.utils import planner


class MultipleGoalPlanDispatcher(Executor):
    def __init__(self, use_local=True):
        self.steps = []
        self.services = None
        self.planner = planner.local if use_local else planner.online

    def initialize(self, services):
        self.services = services

    def next_action(self):
        if not self.steps:
            next_goal = self.services.goal_tracking.uncompleted_goals[-1]

            next_problem = self.services.parser.generate_problem(
                "multiple_goal_temp.pddl",
                self.services.perception.get_state(),
                next_goal,
            )
            self.steps = self.planner(self.services.pddl.domain_path, next_problem)

        return self.steps.pop(0).lower()


class RandomExecutor(Executor):
    """
    RandomExecutor - pick a random valid action each step
    the trick is finding out the valid actions
    Using the tracked successor is significantly faster
    """

    def initialize(self, services):
        self.services = services

    def pick_action_from_many(self, options):
        chosen_action = random.choice(options)

        return chosen_action

    def next_action(self):
        options = self.services.valid_actions.get()

        if len(options) == 0:
            return None
        elif len(options) == 1:
            return options[0]

        return self.pick_action_from_many(options)


class AvoidReturn(Executor):

    def __init__(self):
        pass

    def initialize(self, services):
        self.services = services
        self.previous_state = None
        self.last_different_state = None

    def next_action(self):
        """
        save previous state after choosing next action
        """

        current_state = self.services.perception.get_state()

        if current_state != self.previous_state:
            self.last_different_state = self.previous_state

        self.previous_state = current_state

        options = self.services.valid_actions.get()

        if len(options) == 0:
            return None
        elif len(options) == 1:
            return options[0]

        return self.pick_from_many(options)

    def is_next_state_same_as_previous(self, option):
        next_state = self.services.perception.get_state()

        self.services.parser.apply_action_to_state(option, next_state, False)

        return next_state != (
            self.last_different_state
            if self.previous_state == self.services.perception.get_state()
            else self.previous_state
        )

    def remove_return_actions(self, options):
        if self.previous_state:
            return filter(self.is_next_state_same_as_previous, options)

        return options

    def pick_from_many(self, options):
        options = list(self.remove_return_actions(options))
        return random.choice(options)


class PlanDispatcher(Executor):
    def __init__(self, use_local=True):
        self.steps = []
        self.planner = planner.local if use_local else planner.online

    def initialize(self, services):
        self.steps = self.planner(services.pddl.domain_path, services.pddl.problem_path)

    def next_action(self):
        if len(self.steps) > 0:
            return self.steps.pop(0).lower()

        return None


GENERATED_ROOT = "domains/generated/"
MAZE_DOMAIN = GENERATED_ROOT + "domain.pddl"

"""
This is true by default to avoid using network to run tests.
However this won't work on platforms that don't support local planners
"""
USE_LOCAL_PLANNER_FOR_TESTS = True


def test_parser():
    domain_path, problem_path = (
        MAZE_DOMAIN,
        GENERATED_ROOT + "problems/corridor_5_failable.pddl",
    )
    parser = FDParser(domain_path, problem_path)


def test_libffbug():
    """There was a bug where if the domain was loaded twice there would be a bug"""
    for i in range(2):
        d1 = RandomExecutor()
        LocalSimulator().run(
            MAZE_DOMAIN, GENERATED_ROOT + "problems/simple_problem.pddl", d1
        )


def test_or():
    domain_path, problem_path = MAZE_DOMAIN, GENERATED_ROOT + "problems/t_5_5_5_or.pddl"
    assert LocalSimulator().run(domain_path, problem_path, RandomExecutor()).success


def test_multiple_goals():
    domain_path, problem_path = (
        MAZE_DOMAIN,
        GENERATED_ROOT + "problems/t_5_5_5_multiple.pddl",
    )
    assert (
        LocalSimulator()
        .run(
            domain_path,
            problem_path,
            MultipleGoalPlanDispatcher(USE_LOCAL_PLANNER_FOR_TESTS),
        )
        .success
    )


def test_plan_dispatcher():
    domain_path, problem_path = MAZE_DOMAIN, GENERATED_ROOT + "problems/t_10_10_10.pddl"
    assert (
        LocalSimulator()
        .run(domain_path, problem_path, PlanDispatcher(USE_LOCAL_PLANNER_FOR_TESTS))
        .success
    )


def test_avoid_return():
    domain_path, problem_path = MAZE_DOMAIN, GENERATED_ROOT + "problems/t_5_5_5.pddl"
    assert LocalSimulator().run(domain_path, problem_path, AvoidReturn()).success


def test_failable():
    domain_path, problem_path = (
        GENERATED_ROOT + "domain_failable.pddl",
        GENERATED_ROOT + "problems/corridor_5_failable.pddl",
    )
    assert (
        LocalSimulator(print_actions=True)
        .run(domain_path, problem_path, RandomExecutor())
        .success
    )


def test_multi_effect():
    domain_path, problem_path = (
        GENERATED_ROOT + "domain_multi_effect.pddl",
        GENERATED_ROOT + "problems/corridor_5.pddl",
    )
    assert (
        LocalSimulator(print_actions=True, hide_fails=False, hide_probabilstics=True)
        .run(domain_path, problem_path, RandomExecutor())
        .success
    )


def test_revealable():
    domain_path, problem_path = (
        GENERATED_ROOT + "domain_multi_effect.pddl",
        GENERATED_ROOT + "problems/corridor_5_revealable.pddl",
    )
    assert (
        LocalSimulator(print_actions=True, hide_fails=True, hide_probabilstics=True)
        .run(domain_path, problem_path, RandomExecutor())
        .success
    )
