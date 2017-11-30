import random
import copy

from avoid_return_random import AvoidReturn
from pddlsim.simulator import Simulator
from pddlsim.planner import make_plan


class DelayedDispatch(AvoidReturn):
    def __init__(self,use_lapkt_successor=True):        
        super(DelayedDispatch, self).__init__(use_lapkt_successor)
        self.previous_state = None

    def initilize(self,simulator):
        super(DelayedDispatch, self).initilize(simulator)
        self.simulator = simulator
        self.plan = None
    
    def next_step_in_plan(self):
        if len(self.plan) > 0:
                return self.plan.pop(0).lower()
        return None

    def next_action(self):                
        if not self.plan is None:
            return self.next_step_in_plan()
        choice = self.pick_action()
        self.previous_state = self.simulator.clone_state()
        return choice

    def pick_action(self):        
        if self.stop_at_goal and self.simulator.check_goal():
            return None
        # get all valid actions
        options = self.get_valid_actions()        
        if len(options) == 0: return None
        if len(options) == 1: return options[0]
        if self.previous_state != None:
            options = [option for option in options if self.next_state(option) != self.previous_state]
        # if there is only one options after reducing actions that take you back
        if len(options) == 1: return options[0]
        
        # create pddl_problem for current state
        problem_path = self.simulator.generate_problem('tmp_delayed_dispatch')

        self.plan = make_plan(self.simulator.domain_path,problem_path) 
        return self.next_step_in_plan()
        