import context
import threading

from pddlsim.local_simulator import LocalSimulator
from pddlsim.executors.random_executor import RandomExecutor
from pddlsim.executors.plan_dispatch_multiple_goals import MultipleGoalPlanDispatcher
from pddlsim.executors.plan_dispatch import PlanDispatcher
from pddlsim.executors.avoid_return_random import AvoidReturn
from pddlsim.fd_parser import FDParser
from pddlsim.remote.remote_simulator import RemoteSimulator
from pddlsim.remote.simulator_server import SimulatorForkedTCPServer

GENERATED_ROOT = 'domains/generated/'
MAZE_DOMAIN = GENERATED_ROOT + 'domain.pddl'


def test_parser():
    domain_path, problem_path = MAZE_DOMAIN, GENERATED_ROOT + \
        'problems/corridor_5_failable.pddl'
    parser = FDParser(domain_path, problem_path)


def test_libffbug():
    ''' There was a bug where if the domain was loaded twice there would be a bug
    '''
    for i in range(2):
        d1 = RandomExecutor()
        LocalSimulator().run(
            MAZE_DOMAIN,  GENERATED_ROOT + 'problems/simple_problem.pddl', d1)


def test_or():
    domain_path, problem_path = MAZE_DOMAIN, GENERATED_ROOT + \
        'problems/t_5_5_5_or.pddl'
    assert LocalSimulator().run(
        domain_path, problem_path, RandomExecutor()).success


def test_multiple_goals():
    domain_path, problem_path = MAZE_DOMAIN, GENERATED_ROOT + \
        'problems/t_5_5_5_multiple.pddl'
    assert LocalSimulator().run(
        domain_path, problem_path, MultipleGoalPlanDispatcher(True)).success


def test_avoid_return():
    domain_path, problem_path = MAZE_DOMAIN, GENERATED_ROOT + \
        'problems/t_5_5_5.pddl'
    assert LocalSimulator().run(
        domain_path, problem_path, AvoidReturn()).success


def test_failable():
    domain_path, problem_path = GENERATED_ROOT + \
        'domain_failable.pddl', GENERATED_ROOT + \
        'problems/corridor_5_failable.pddl'
    executives = [RandomExecutor()]
    assert LocalSimulator(
        print_actions=True).run(
        domain_path, problem_path, RandomExecutor()).success


def test_multi_effect():
    domain_path, problem_path = GENERATED_ROOT + \
        'domain_multi_effect.pddl', GENERATED_ROOT + \
        'problems/corridor_5.pddl'
    executives = [RandomExecutor()]
    assert LocalSimulator(
        print_actions=True, hide_fails=False, hide_probabilstics=True).run(
        domain_path, problem_path, RandomExecutor()).success


def test_revealable():
    domain_path, problem_path = GENERATED_ROOT + \
        'domain_multi_effect.pddl', GENERATED_ROOT + \
        'problems/corridor_5_revealable.pddl'
    assert LocalSimulator(
        print_actions=True, hide_fails=True, hide_probabilstics=True).run(
        domain_path, problem_path, RandomExecutor()).success
