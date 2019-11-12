import context
from pddlsim.local_simulator import LocalSimulator
from pddlsim.executors.random_executor import RandomExecutor
from pddlsim.executors.plan_dispatch_multiple_goals import MultipleGoalPlanDispatcher
from pddlsim.fd_parser import FDParser

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
        domain_path, problem_path, MultipleGoalPlanDispatcher()).success


def test_avoid_return():
    pass


def test_failable():
    pass


def test_multi_effect():
    pass


def test_revealable():
    pass


def test_remote():
    pass
