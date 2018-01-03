from pddl import PDDL
from goal_tracking import GoalTracking
from valid_actions import TrackedSuccessorValidActions, PythonValidActions
from problem_generator import ProblemGenerator

class SimulatorMediator():
    def __init__(self, simulator):

        self.pddl = PDDL(simulator.domain_path,simulator.problem_path)
        self.goal_tracking = GoalTracking(simulator)

        self.valid_actions = TrackedSuccessorValidActions(simulator,self.goal_tracking)
        self.memorizer = Memorizer(simulator)
        self.action_simulator = ActionSimulator(simulator)
        self.problem_generator = ProblemGenerator(simulator, self.goal_tracking, "tmp_problem_generation")


class Memorizer():
    def __init__(self, simulator):
        self.previous_state = None
        self.simulator = simulator

    def save_state(self):
        self.previous_state = self.simulator.clone_state()

    def load_state(self):
        return self.previous_state

    def has_state(self):
        return self.previous_state is not None

class ActionSimulator():
    def __init__(self, simulator):
        self.simulator = simulator

    def next_state(self, action):
        next_state = self.simulator.clone_state()
        self.simulator.act(action, next_state)
        return next_state
