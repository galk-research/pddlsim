from pddlsim.services import (pddl, goal_tracking,problem_generator,memorizer,action_simulator,valid_actions)
from pddlsim.fd_parser import FDParser

class RemoteSimulatorMediator():
    def __init__(self, simulator):
        
        self.pddl = pddl.PDDL(simulator.domain_path,simulator.problem_path)
        self.parser = FDParser(simulator.domain_path,simulator.problem_path)
        self.perception = simulator
        self.goal_tracking = goal_tracking.GoalTracking(self.parser,self.perception.get_state)        

        self.problem_generator = problem_generator.ProblemGenerator(self.perception, self.parser, "tmp_problem_generation")
        
        self.memorizer = memorizer.Memorizer(self.perception)
        # self.action_simulator = action_simulator.ActionSimulator(simulator)
        
        self.valid_actions = valid_actions.TrackedSuccessorValidActions(self.pddl, self.problem_generator, self.goal_tracking)
        
    def on_action(self, action_sig):        
        self.goal_tracking.on_action()        
        self.valid_actions.on_action(action_sig)
