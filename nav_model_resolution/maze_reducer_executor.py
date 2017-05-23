from executor import Executor
import planner
import reduce_domain

class MazeReducerExecutor(Executor):    
    def __init__(self):
        super(MazeReducerExecutor, self).__init__()
        self.steps = []

    def initilize(self,sim):     
        temp_path = 'temp_reduced.pddl'
        
        self.graph = reduce_domain.reduce_problem(sim.domain_path, sim.problem_path, temp_path)
        self.big_steps = planner.make_plan(sim.domain_path,temp_path)

        # self.expanded_steps = [ for step in big_steps]


    def next_action(self):
        if len(self.steps) > 0:
            return self.steps.pop(0).lower()
        return None
