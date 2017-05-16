from simulator import Simulator
from plan_dispatch import PlanDispatcher
from random_executor import RandomExecutor
import planner
if __name__ == '__main__':

    #works:
    domain_path,problem_path = 'domains/Log_dom.pddl','domains/Log_ins.pddl'
    # domain_path,problem_path = 'domain.pddl','problem.pddl'

    #doesn't work:
    # domain_path,problem_path = 'domains/Mapana_dom.pddl','domains/Mapana_ins.pddl'
    # domain_path,problem_path = 'domains/Sched_dom.pddl','domains/Sched_ins.pddl'
    # domain_path,problem_path = 'domains/Elev_dom.pddl','domains/Elev_ins.pddl'

    # print(planner.make_plan(domain_path,problem_path))
    # exit()
    
    
    executor = PlanDispatcher()
    # executor = RandomExecutor(stop_at_goal=False)
    sim = Simulator(domain_path)
    sim.begin(problem_path, executor)
    if sim.reached_goal:
        print('Reached goal!')
    else:
        print('Failed to reach goal')
