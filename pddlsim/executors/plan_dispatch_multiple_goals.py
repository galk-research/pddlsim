from executor import Executor
import pddlsim.planner as planner

class MultipleGoalPlanDispatcher(Executor):
    """docstring for PlanDispatcher."""
    def __init__(self):
        super(MultipleGoalPlanDispatcher, self).__init__()
        self.steps = []     
        self.simulator = None   

    def initilize(self,sim):
        self.simulator = sim
        
    def next_action(self):        
        if not self.steps and self.simulator.uncompleted_goals:
            if self.simulator.reached_all_goals:
                return None
            next_goal = self.simulator.uncompleted_goals[-1]
            print next_goal
            # get only one goal
            next_problem = self.simulator.generate_problem('multiple_goal_temp.pddl',next_goal)
            self.steps = planner.make_plan(self.simulator.domain_path,next_problem)            
        
        if self.steps:
            return self.steps.pop(0).lower()
        
        return None
