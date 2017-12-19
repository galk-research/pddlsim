import sys, os
sys.path.insert(0, os.path.abspath('..'))

from pddlsim.simulator import Simulator
from pddlsim.executors.plan_dispatch_multiple_goals import MultipleGoalPlanDispatcher
from pddlsim.executors.random_executor import RandomExecutor
from pddlsim.executors.delayed_dispatch import DelayedDispatch

def simulate(executor, domain_path, problem_path):    
    sim = Simulator(domain_path)
    sim.simulate(problem_path, executor)
    if sim.reached_all_goals:
        print('Reached goal!')
    else:
        print('Failed to reach goal')

if __name__ == '__main__':
    domain_path, problem_path = 'domain.pddl','problems/t_5_5_5_multiple.pddl'
    simulate(MultipleGoalPlanDispatcher(), domain_path, problem_path)
    # simulate(RandomExecutor(), domain_path, problem_path)
    

    