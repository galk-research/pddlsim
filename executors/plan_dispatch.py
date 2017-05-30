from executors.executor import Executor
import planner

class PlanDispatcher(Executor):
    """docstring for PlanDispatcher."""
    def __init__(self):
        super(PlanDispatcher, self).__init__()
        self.steps = []

    def initilize(self,sim):        
        self.steps = planner.make_plan(sim.domain_path,sim.problem_path)        

    def next_action(self):
        if len(self.steps) > 0:
            return self.steps.pop(0).lower()
        return None
