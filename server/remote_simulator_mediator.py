from pddlsim.services import (pddl, goal_tracking)
from pddlsim.fd_parser import FDParser

class RemoteSimulatorMediator():
    def __init__(self, simulator):
        
        self.pddl = pddl.PDDL(simulator.domain_path,simulator.problem_path)
        self.parser = FDParser(simulator.domain_path,simulator.problem_path)
        self.perception = simulator
        self.goal_tracking = goal_tracking.GoalTracking(self.parser,self.perception.get_state)        

        # self.valid_actions = TrackedSuccessorValidActions(simulator,self.goal_tracking)
        # self.memorizer = memorizer.Memorizer(simulator)
        # self.action_simulator = action_simulator.ActionSimulator(simulator)
        # self.problem_generator = problem_generator.ProblemGenerator(simulator, self.goal_tracking, "tmp_problem_generation")
    
    def on_action(self):
        self.goal_tracking.on_action()        
