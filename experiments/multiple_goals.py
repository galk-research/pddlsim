import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from pddlsim.simulator import Simulator
from pddlsim.executors.plan_dispatch_multiple_goals import MultipleGoalPlanDispatcher
from pddlsim.executors.random_executor import RandomExecutor
from pddlsim.executors.delayed_dispatch import DelayedDispatch
from pddlsim.sim_env import SimEnv

if __name__ == '__main__':
    domain_path, problem_path = 'domain.pddl', 'problems/t_5_5_5_multiple.pddl'
    print SimEnv().run(domain_path, problem_path, MultipleGoalPlanDispatcher())
