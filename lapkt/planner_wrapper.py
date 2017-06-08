from lapkt.libfdplanner import Planner 

# class for profiling purposes
class Planner_Wrapper(object):
    def __init__(self):
        self.task = Planner()
    
    def setup(self):
        self.task.setup()

    def create_state(self,encoded):
        return self.task.create_state(encoded)
    
    def next_actions(self,state):
        return self.task.next_actions(state)
