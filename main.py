from __future__ import print_function

import glob
import os
import time

from pddlsim.simulator import Simulator,compare_executors
from pddlsim.executors.plan_dispatch import PlanDispatcher
from pddlsim.executors.random_executor import RandomExecutor
from pddlsim.executors.avoid_return_random import AvoidReturn
from pddlsim.executors.delayed_dispatch import DelayedDispatch
from pddlsim.executors import executor
from experiments import reduce_domain,generate_problem
from experiments.maze_reducer_executor import MazeReducerExecutor

import pddlsim.planner

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

def compare_many():

    # length = 400
    # domain_path, problem_path = "ipc2002/zenotravel/domain.pddl","ipc2002/zenotravel/prob01.pddl"
    # domain_path,problem_path = 'experiments/domain.pddl',generate_problem.generate_corridor(length)
    domain_path = 'experiments/domain.pddl'
    # problems = [generate_problem.generate_T(i,5,5) for i in [100,200,300,400]]

    # executors = {'PlanDispatcher':PlanDispatcher(), 'MazeReducerExecutor':MazeReducerExecutor()}
    # executors = {'PlanDispatcher':PlanDispatcher(), 'Random':RandomExecutor()}
    # executors = {'No_Return':AvoidReturn(use_lapkt_successor=False),'PlanDispatcher':PlanDispatcher()}
    problem = generate_problem.generate_T(50,5,5)
    executors = {'PlanDispatcher':PlanDispatcher(), 'DelayedDispatch':DelayedDispatch()}
    print(compare_executors(domain_path,problem,executors))


def simulate(executor, domain_path, problem_path):
    sim = Simulator(domain_path)
    # sim.print_actions = False
    sim.simulate(problem_path, executor)
    if sim.reached_all_goals:
        print('Reached goal!')
    else:
        print('Failed to reach goal')


def profile():
    import pstats
    import cProfile

    target = 'delayed_dispatch'

    profile_path = os.path.join('profile',target)

    executives = {'avoid_run_lapkt':'AvoidReturn(use_lapkt_successor=True)',
                  'avoid_run':'AvoidReturn(use_lapkt_successor=False)',
                  'plan_dispatch':'PlanDispatcher()',
                  'delayed_dispatch':'DelayedDispatch()'}
    code = 'simulate('+executives[target] +',domain_path,problem_path)'

    # run profiling
    cProfile.run(code, profile_path)

    # print the results
    p = pstats.Stats(profile_path)
    p.strip_dirs().sort_stats('tottime').print_stats('')

    # for profile_path in glob.glob("profile/*"):
    #     if not profile_path.endswith('.txt'):
    #         p = pstats.Stats(profile_path)
    #         p.strip_dirs().sort_stats('cumtime').print_stats('simulator')

    # use a graph tool to profile

    # from pycallgraph import PyCallGraph
    # from pycallgraph.output import GraphvizOutput
    # graphviz = GraphvizOutput()
    # graphviz.output_file = 'basic.png'

    # with PyCallGraph(output=graphviz):
    #     simulate(AvoidReturn(use_lapkt_successor=True), domain_path, problem_path)

def libffbug():
    domain_path,problem_path = 'experiments/domain.pddl','experiments/problems/simple_problem.pddl'
    for i in range(2):
        d1 = RandomExecutor()
        sim = Simulator(domain_path,print_actions=True)
        sim.simulate(problem_path, d1)

    # d2 = RandomExecutor()
    # sim = Simulator(domain_path,print_actions=False)
    # sim.simulate(problem_path, d2)

import os
import sys
import threading


class OutputGrabber(object):
    """
    Class used to grab standard output or another stream.
    """
    escape_char = "\b"

    def __init__(self, stream=None, threaded=False):
        self.origstream = stream
        self.threaded = threaded
        if self.origstream is None:
            self.origstream = sys.stdout
        self.origstreamfd = self.origstream.fileno()        
        # Create a pipe so the stream can be captured:
        self.pipe_out, self.pipe_in = os.pipe()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def start(self):                
        # Save a copy of the stream:
        self.streamfd = os.dup(self.origstreamfd)
        # Replace the original stream with our write pipe:
        os.dup2(self.pipe_in, self.origstreamfd)      

    def stop(self):
        """
        Stop capturing the stream data and save the text in `capturedtext`.
        """
        # Print the escape character to make the readOutput method stop:
        self.origstream.write(self.escape_char)
        # Flush the stream to make sure all our data goes in before
        # the escape character:
        self.origstream.flush()        
        self.readOutput()
        # Close the pipe:
        os.close(self.pipe_out)
        # Restore the original stream:
        os.dup2(self.streamfd, self.origstreamfd)

    def readOutput(self):
        """
        Read the stream data (one byte at a time)
        and save the text in `capturedtext`.
        """
        while True:
            char = os.read(self.pipe_out, 1)
            if not char or self.escape_char in char:
                break

if __name__ == '__main__':

    # compare_many()
    # test_all_ipc2002()
    # profile()
    # with OutputGrabber():
    #     libffbug()
    
    # print('Done')
    # exit()

    #works:
    # domain_path,problem_path = 'domains/Log_dom.pddl','domains/Log_ins.pddl'

    #doesn't work:
    # domain_path,problem_path = 'domains/Mapana_dom.pddl','domains/Mapana_ins.pddl'    
    # domain_path,problem_path = 'domains/Sched_dom.pddl','domains/Sched_ins.pddl'
    # domain_path,problem_path = 'domains/Elev_dom.pddl','domains/Elev_ins.pddl'

    # domain_path,problem_path = 'experiments/domain.pddl','experiments/problems/simple_problem.pddl'
    # domain_path,problem_path = 'experiments/domain.pddl','experiments/problems/corridor_5.pddl'
    domain_path,problem_path = 'experiments/domain.pddl','experiments/problems/t_5_5_5.pddl'

    executives = [PlanDispatcher(),RandomExecutor(),AvoidReturn(),DelayedDispatch()]
    results = dict()
    for executive in executives:                
        results[executive.__class__.__name__] = False            
        try:
            with OutputGrabber():
                simulate(executive,domain_path,problem_path)
            results[executive.__class__.__name__] = True
        except:
            pass
        
    print (results)
    exit()
