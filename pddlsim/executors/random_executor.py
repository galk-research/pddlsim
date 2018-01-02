# import pddl.parsersimulate
import random
# from pddlsim.successors.successor import Successor
from pddlsim.successors.tracked_successor import TrackedSuccessor

class RandomExecutor(object):
    """ RandomExecutor - pick a random valid action each step
        the trick is finding out the valid actions
        Most of the code here is a python implementation of that
        But using the tracked successor is significantly faster
    """
    def __init__(self,stop_at_goal=True,use_lapkt_successor=True):
        super(RandomExecutor, self).__init__()
        self.stop_at_goal = stop_at_goal
        self.use_lapkt_successor = use_lapkt_successor
        self.successor = None

    def initilize(self,services):
        self.services = services        

    def next_action(self):
        if self.stop_at_goal and self.services.goal_tracking.reached_all_goals():
            return None
        # get all valid actions
        possible_actions = [] if self.stop_at_goal else [None]
        options = self.services.valid_actions.get() + possible_actions
        if len(options) == 0: return None
        chosen = random.choice(options)
        return chosen
