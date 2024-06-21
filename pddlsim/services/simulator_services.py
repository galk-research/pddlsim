from pddlsim.services.pddl import PDDL
from pddlsim.services.goal_tracking import GoalTracking
from pddlsim.services.valid_actions import ValidActions
from pddlsim.services.perception import Perception
from pddlsim.fd_parser import FDParser


class SimulatorServices():

    def __init__(self, parser, perception_func):
        self.parser = parser
        self.perception = Perception(perception_func)
        self.goal_tracking = GoalTracking(self.parser, self.perception)

        problem_path = self.parser.problem_path

        if self.parser.uses_custom_features:
            problem_path = "tmp_problem_generation"
            self.parser.generate_problem(problem_path, self.perception.get_state(), self.parser.goals[0])
            self.parser.problem_path = problem_path
        self.pddl = PDDL(parser.domain_path, problem_path)

        self.valid_actions = ValidActions(self.parser, self.perception)
        self.on_action_observers = [self.perception.on_action,
                                    self.valid_actions.on_action,
                                    self.goal_tracking.on_action, ]

    @staticmethod
    def from_pddls(domain_path, problem_path, perception_func):
        parser = FDParser(domain_path, problem_path)
        return SimulatorServices(parser, perception_func)

    def on_action(self, action_sig):
        if action_sig is None:
            return
        for func in self.on_action_observers:
            func(action_sig)
