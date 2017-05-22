# import pddl.parser
import random

class RandomExecutor(object):
    """docstring for RandomExecutor."""
    def __init__(self,stop_at_goal=True):        
        super(RandomExecutor, self).__init__()
        self.stop_at_goal = stop_at_goal

    def initilize(self,simulator):
        self.simulator = simulator

    def next_action(self):
        if self.stop_at_goal and self.simulator.check_goal():
            return None
        # get all valid actions
        options = self.get_valid_actions()
        if len(options) == 0: return None
        chosen = random.choice(options)
        # print(chosen)
        return chosen
    
    def get_valid_candidates_for_action(self,action):
        '''
        Get all the valid parameters for a given action for the current state of the simulation
        '''
        objects = dict()
        candidates = []
        #copy all preconditions
        precondition_left = self.simulator.parser.get_action_preconditions(action)[:]
        for (name,t) in self.simulator.parser.get_action_signature(action):            
            objects[name] = t

            # add all possible objects of the type
            matching_objects = self.simulator.parser.get_objects_of_type(t)            

            # filter predicates that can be tested at this stage
            preconditions_to_test = []
            for precondition in precondition_left:
                if self.simulator.parser.has_all_objects(precondition, objects):
                    preconditions_to_test.append(precondition)
            for pre in preconditions_to_test:
                precondition_left.remove(pre)

            new_candidates = []
            if len(objects) == 1:
                for instance in matching_objects:
                    new_candidates.append({name:instance})
            else:
                for previous_candidate in candidates:
                    for instance in matching_objects:
                        candidate = previous_candidate.copy()
                        candidate[name] = instance
                        new_candidates.append(candidate)
            # maybe this can happed while building candidates
            for precondition in preconditions_to_test:
                new_candidates[:] = [c for c in new_candidates if self.simulator.test_predicate(precondition.name,precondition.signature,c)]

            candidates = new_candidates
        return candidates

    def get_valid_actions(self):
        possible_actions = [] if self.stop_at_goal else [None]
        for (name,action) in self.simulator.parser.get_actions():
            for candidate in self.get_valid_candidates_for_action(action):
                possible_actions.append(self.simulator.parser.get_action_string(action,candidate))
        return possible_actions
    
   