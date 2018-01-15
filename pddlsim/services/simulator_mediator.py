from pddl import PDDL
from goal_tracking import GoalTracking
from valid_actions import TrackedSuccessorValidActions, PythonValidActions
from problem_generator import ProblemGenerator
from memorizer import Memorizer
from action_simulator import ActionSimulator

class SimulatorMediator():
    def __init__(self, simulator):

        self.pddl = PDDL(simulator.domain_path,simulator.problem_path)
        self.goal_tracking = GoalTracking(simulator)

        self.valid_actions = TrackedSuccessorValidActions(simulator,self.goal_tracking)
        self.memorizer = Memorizer(simulator)
        self.action_simulator = ActionSimulator(simulator)
        self.problem_generator = ProblemGenerator(simulator, self.goal_tracking, "tmp_problem_generation")
