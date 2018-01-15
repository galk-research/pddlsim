from pddlsim.services import *

class RemoteSimulatorMediator():
    def __init__(self, simulator):

        self.pddl = pddl.PDDL(simulator.domain_path,simulator.problem_path)
        # self.goal_tracking = goal_tracking.GoalTracking(simulator)

        # self.valid_actions = TrackedSuccessorValidActions(simulator,self.goal_tracking)
        # self.memorizer = memorizer.Memorizer(simulator)
        # self.action_simulator = action_simulator.ActionSimulator(simulator)
        # self.problem_generator = problem_generator.ProblemGenerator(simulator, self.goal_tracking, "tmp_problem_generation")
