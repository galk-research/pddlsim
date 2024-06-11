from executor import Executor
from pddlsim.utils import planner


class MultipleGoalPlanDispatcher(Executor):

    """docstring for PlanDispatcher."""

    def __init__(self, use_local=True):
        super(MultipleGoalPlanDispatcher, self).__init__()
        self.steps = []
        self.services = None
        self.planner = planner.local if use_local else planner.online

    def initialize(self, services):
        self.services = services

    def next_action(self):
        if not self.steps and self.services.goal_tracking.uncompleted_goals:
            if self.services.goal_tracking.reached_all_goals():
                return None
            next_goal = self.services.goal_tracking.uncompleted_goals[-1]
            print next_goal
            # get only one goal
            next_problem = self.services.parser.generate_problem("multiple_goal_temp.pddl", self.services.perception.get_state(), next_goal)
            self.steps = self.planner(
                self.services.pddl.domain_path, next_problem)

        if self.steps:
            return self.steps.pop(0).lower()

        return None
