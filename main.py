from simulator import Simulator
from plan_dispatch import PlanDispatcher
from random_executor import RandomExecutor
from nav_model_resolution import reduce_domain
import planner
import glob
import os

import first_parser

def test_all_ipc2002():
     for domain_dir in glob.glob('ipc2002/*'):    
        
        domain_path = os.path.join(domain_dir,'domain.pddl')
        problem_path = os.path.join(domain_dir,'prob01.pddl')
        # first_parser.FirstParser(domain_path,problem_path)
        executor = PlanDispatcher()

        sim = Simulator(domain_path,print_actions=False)
        sim.simulate(problem_path, executor)
        if sim.reached_goal:
            print('Reached goal!',)
        else:
            print('Failed to reach goal',)


if __name__ == '__main__':

    
    #works:
    # domain_path,problem_path = 'domains/Log_dom.pddl','domains/Log_ins.pddl'
    
    #doesn't work:
    # domain_path,problem_path = 'domains/Mapana_dom.pddl','domains/Mapana_ins.pddl'
    # domain_path,problem_path = 'domains/Sched_dom.pddl','domains/Sched_ins.pddl'
    # domain_path,problem_path = 'domains/Elev_dom.pddl','domains/Elev_ins.pddl'

    # domain_path,problem_path = 'nav_model_resolution/domain.pddl','nav_model_resolution/simple_problem.pddl'
    domain_path,problem_path = 'nav_model_resolution/domain.pddl','nav_model_resolution/corridor_5.pddl'

    # print(planner.make_plan(domain_path,problem_path))
    reduce_domain.reduce_problem(domain_path,problem_path)
    exit()
    
    executor = PlanDispatcher()
    # executor = RandomExecutor(stop_at_goal=False)
    sim = Simulator(domain_path)
    sim.simulate(problem_path, executor)
    if sim.reached_goal:
        print('Reached goal!')
    else:
        print('Failed to reach goal')
