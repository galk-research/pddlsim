from pddlsim.simulator import Simulator
from pddlsim.executors.plan_dispatch import PlanDispatcher

def simulate(executor, domain_path, problem_path):    
    sim = Simulator(domain_path)
    sim.simulate(problem_path, executor)
    if sim.reached_goal:
        print('Reached goal!')
    else:
        print('Failed to reach goal')

if __name__ == '__main__':
    domain_path,problem_path = 'domain.pddl','problems/t_5_5_5_multiple.pddl'
    simulate(PlanDispatcher(),domain_path,problem_path)
    
    