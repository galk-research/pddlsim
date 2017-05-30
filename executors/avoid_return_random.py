from executors.random_executor import RandomExecutor
from simulator import Simulator
import random
import copy

class AvoidReturn(RandomExecutor):
    def __init__(self):        
        super(AvoidReturn, self).__init__(True)
        self.previous_state = None

    def initilize(self,simulator):
        self.simulator = simulator

    def next_action(self):        
        ''' 
        save previous state after choosing next action
        '''
        choice = self.pick_action()
        self.previous_state = copy.deepcopy(self.simulator.state)
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
            
        chosen = random.choice(options)
        # print(chosen)
        return chosen

    def next_state(self, action):
        original_state = copy.deepcopy(self.simulator.state)        
        original_print_actions = self.simulator.print_actions
        self.simulator.print_actions = False
        self.simulator.act(action)
        next_state = self.simulator.state        
        self.simulator.state = original_state
        self.simulator.print_actions = original_print_actions
        return next_state