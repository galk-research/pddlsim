# echo_client.py
# from pddlsim.executors.plan_dispatch import PlanDispatcher
from experiments.maze_reducer_executor import MazeReducerExecutor
from pddlsim.executors import (plan_dispatch,random_executor,avoid_return_random,delayed_dispatch)
from server.client_utils import *

HOST, PORT = "localhost", 9999

if __name__ == '__main__':
    domain_path = './experiments/domain.pddl'
    # problem_path = './experiments/problems/corridor_100.pddl'
    problem_path = './experiments/problems/t_5_5_5.pddl'
    
    executives = [plan_dispatch.PlanDispatcher(),random_executor.RandomExecutor(),avoid_return_random.AvoidReturn(),delayed_dispatch.DelayedDispatch()]

    results = dict()
    for executive in executives:                 
        results[executive.__class__.__name__] = False            
        try:
            with RemoteSimulator(HOST, PORT) as sim:
                sim.use_domain_and_problem(domain_path, problem_path)
                results[executive.__class__.__name__] = sim.simulate(executive)                
        except Exception as e:
            pass     
    for ex,rc in results.iteritems():        
        print ex
        print str(rc)    
