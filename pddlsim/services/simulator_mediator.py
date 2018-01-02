from pddl import PDDL
from goal_tracking import GoalTracking
from valid_actions import TrackedSuccessorValidActions, PythonValidActions

class SimulatorMediator():
    def __init__(self, simulator):
        self.pddl = PDDL(simulator.domain_path,simulator.problem_path)
        self.goal_tracking = GoalTracking(len(simulator.uncompleted_goals) > 1, lambda : simulator.reached_all_goals)
        self.valid_actions = TrackedSuccessorValidActions(simulator,self.goal_tracking)
