# echo_client.py
from pddlsim.executors.plan_dispatch import PlanDispatcher
from experiments.maze_reducer_executor import MazeReducerExecutor

from server.client_utils import *

HOST, PORT = "localhost", 9999

if __name__ == '__main__':
    domain_path = './experiments/domain.pddl'
    problem_path = './experiments/problems/corridor_100.pddl'

    with RemoteSimulator(HOST, PORT) as sim:
        sim.use_domain_and_problem(domain_path, problem_path)
        sim.simulate(PlanDispatcher())
        print str(sim.report_card)
