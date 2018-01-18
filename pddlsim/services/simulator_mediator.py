from pddl import PDDL
from goal_tracking import GoalTracking
from valid_actions import TrackedSuccessorValidActions, PythonValidActions
from problem_generator import ProblemGenerator
from memorizer import Memorizer
from action_simulator import ActionSimulator
from perception import Perception

class SimulatorMediator():
    def __init__(self, simulator):

        self.pddl = PDDL(simulator.domain_path,simulator.problem_path)
        self.perception = Perception(simulator)
        self.goal_tracking = GoalTracking(simulator.parser,self.perception.get_state)
        self.problem_generator = ProblemGenerator(self.perception, simulator.parser, "tmp_problem_generation")
        
        self.memorizer = Memorizer(self.perception)
        self.action_simulator = ActionSimulator(simulator)
        
        self.valid_actions = TrackedSuccessorValidActions(self.pddl, self.problem_generator, self.goal_tracking)
        simulator.on_action += self.on_action

    def on_action(self, sim, action_sig):
        self.goal_tracking.on_action()        
        self.valid_actions.on_action(action_sig)
