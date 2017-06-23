from __future__ import print_function
from simulator import Simulator
from executors.plan_dispatch import PlanDispatcher
from executors.random_executor import RandomExecutor
from executors.avoid_return_random import AvoidReturn
from executors.delayed_dispatch import DelayedDispatch
from executors import executor
from nav_model_resolution import reduce_domain,generate_problem
from nav_model_resolution.maze_reducer_executor import MazeReducerExecutor
from lapkt.successors import Successors 

import planner
import glob
import os

# import first_parser
import time

import cProfile

IPC_PATH = 'ipc2002/'
def test_all_ipc2002():
     for domain_dir in glob.glob(IPC_PATH + '*')[2:]:    
        
        domain_path = os.path.join(domain_dir,'domain.pddl')
        count, total = 0, 0
        for problem_path in glob.glob(domain_dir+'/prob*.pddl'):        
            print (problem_path)
            executor = PlanDispatcher()
            sim = Simulator(domain_path,print_actions=False)
            sim.simulate(problem_path, executor)
            if sim.reached_goal:
                count += 1
            total += 1
        print(count,total,sep='/')



def compare_executors():
    # length = 400
    # domain_path, problem_path = "ipc2002/zenotravel/domain.pddl","ipc2002/zenotravel/prob01.pddl"
    # domain_path,problem_path = 'nav_model_resolution/domain.pddl',generate_problem.generate_corridor(length)
    domain_path,problem_path = 'nav_model_resolution/domain.pddl',generate_problem.generate_T(400,5,5)
    # executors = {'PlanDispatcher':PlanDispatcher(), 'MazeReducerExecutor':MazeReducerExecutor()}    
    # executors = {'PlanDispatcher':PlanDispatcher(), 'Random':RandomExecutor()}    
    # executors = {'No_Return':AvoidReturn(use_lapkt_successor=False),'PlanDispatcher':PlanDispatcher()}    
    executors = {'PlanDispatcher':PlanDispatcher(), 'DelayedDispatch':DelayedDispatch()}    
    
    for name, executor in executors.items():        
        t0 = time.time()
        
        sim = Simulator(domain_path,print_actions=False)
        sim.simulate(problem_path, executor)
                
        t1 = time.time()

        total = t1-t0
        print(name, total)

def simulate(executor, domain_path, problem_path):    
    sim = Simulator(domain_path)
    # sim.print_actions = False
    sim.simulate(problem_path, executor)
    if sim.reached_goal:
        print('Reached goal!')
    else:
        print('Failed to reach goal')

def successors():
    domain_path,problem_path = 'nav_model_resolution/domain.pddl','nav_model_resolution/corridor_5.pddl'        
    
    # domain_path, problem_path = "ipc2002/zenotravel/domain.pddl","ipc2002/zenotravel/prob01.pddl"
    sim = Simulator(domain_path)
    sim.simulate(problem_path,executor.Executor())
    succ = Successors(domain_path,problem_path)
    # print(list(succ.expand_simulator_state(sim.state)))
    res = succ.next(sim.state)
    for r in res: 
        print (r)
    

import pstats

if __name__ == '__main__':
    
    # successors()
    compare_executors()
    # test_all_ipc2002()
    exit()
    
    #works:
    # domain_path,problem_path = 'domains/Log_dom.pddl','domains/Log_ins.pddl'
    
    #doesn't work:
    # domain_path,problem_path = 'domains/Mapana_dom.pddl','domains/Mapana_ins.pddl'
    # domain_path,problem_path = 'domains/Sched_dom.pddl','domains/Sched_ins.pddl'
    # domain_path,problem_path = 'domains/Elev_dom.pddl','domains/Elev_ins.pddl'

    # domain_path,problem_path = 'nav_model_resolution/domain.pddl','nav_model_resolution/simple_problem.pddl'
    # domain_path,problem_path = 'nav_model_resolution/domain.pddl','nav_model_resolution/corridor_5.pddl'
    domain_path,problem_path = 'nav_model_resolution/domain.pddl','nav_model_resolution/t_5_5_5.pddl'

    # 2 random executors cause segmentation fault
    # d1 = RandomExecutor()    
    # d2 = RandomExecutor()
    # sim = Simulator(domain_path,print_actions=False)
    # sim.simulate(problem_path, d1)
    from lapkt.tracked_successor import TrackedSuccessors
    
    # sim = Simulator(domain_path,print_actions=False)
    # sim.problem_path = problem_path
    # # sim.simulate(problem_path, d2)
    
    # t1 = TrackedSuccessors(sim)
    # t1.proceed('(MOVE-EAST PERSON1 START_TILE C0)')

    # sim = Simulator(domain_path,print_actions=False)
    # sim.problem_path = problem_path
    # # sim.simulate(problem_path, d2)
    
    # # from lapkt.tracked_successor import TrackedSuccessors
    # t1 = TrackedSuccessors(sim)
    # t1.proceed('(MOVE-EAST PERSON1 START_TILE C0)')
    exit()
        
    # simulate(PlanDispatcher(),domain_path,problem_path)
    # simulate(RandomExecutor(stop_at_goal=True),domain_path,problem_path)
    # simulate(MazeReducerExecutor(),domain_path,problem_path)
    # simulate(DelayedDispatch(),domain_path,problem_path)

    # exit()
    # profile_path = 'profile/avoid_run_lapkt'
    # cProfile.run('simulate(AvoidReturn(use_lapkt_successor=True), domain_path, problem_path)',profile_path)

    # profile_path = 'profile/avoid_run'
    # cProfile.run('simulate(AvoidReturn(use_lapkt_successor=False), domain_path, problem_path)',profile_path)


    # profile_path = 'profile/plan_dispatch'
    # cProfile.run('simulate(PlanDispatcher(),domain_path,problem_path)',profile_path)
    
    profile_path = 'profile/delayed_dispatch'    
    cProfile.run('simulate(DelayedDispatch(),domain_path,problem_path)',profile_path)

    p = pstats.Stats(profile_path)
    p.strip_dirs().sort_stats('tottime').print_stats('')

    # for profile_path in glob.glob("profile/*"):
    #     if not profile_path.endswith('.txt'):
    #         p = pstats.Stats(profile_path)
    #         p.strip_dirs().sort_stats('cumtime').print_stats('simulator')

    # from pycallgraph import PyCallGraph
    # from pycallgraph.output import GraphvizOutput
    # graphviz = GraphvizOutput()
    # graphviz.output_file = 'basic.png'

    # with PyCallGraph(output=graphviz):
    #     simulate(AvoidReturn(use_lapkt_successor=True), domain_path, problem_path)
    
