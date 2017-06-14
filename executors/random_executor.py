# import pddl.parsersimulate
import random
from lapkt.successors import Successors

class RandomExecutor(object):
    """docstring for RandomExecutor."""
    def __init__(self,stop_at_goal=True,use_lapkt_successor=True):        
        super(RandomExecutor, self).__init__()
        self.stop_at_goal = stop_at_goal
        self.use_lapkt_successor = use_lapkt_successor
        self.successors = None

    def initilize(self,simulator):
        self.simulator = simulator
        if self.use_lapkt_successor:
            self.successor = Successors(self.simulator.domain_path,self.simulator.problem_path)

    def next_action(self):
        if self.stop_at_goal and self.simulator.check_goal():
            return None
        # get all valid actions
        options = self.get_valid_actions()
        if len(options) == 0: return None
        chosen = random.choice(options)
        # print(chosen)
        return chosen
    
    def get_valid_actions(self):
        if self.use_lapkt_successor:
            return self.successor.next(self.simulator.state)
        possible_actions = [] if self.stop_at_goal else [None]
        for (name,action) in self.simulator.parser.actions.items():
            for candidate in self.get_valid_candidates_for_action(action):
                possible_actions.append(action.action_string(candidate))
        return possible_actions

    def join_candidates(self, previous_candidates, new_candidates, p_indexes, n_indexes):
        shared_indexes = p_indexes.intersection(n_indexes)            
        if previous_candidates is None: return new_candidates
        result = []
        for c1 in previous_candidates:
            for c2 in new_candidates:
                if all([c1[idx] == c2[idx] for idx in shared_indexes]):
                    merged = c1[:]
                    for idx in n_indexes:
                        merged[idx] = c2[idx]
                    result.append(merged)
        return result        
    

    def indexed_candidate_to_dict(self, candidate, index_to_name):
        return {name[0]:candidate[idx] for idx, name in index_to_name.items()}

    def get_valid_candidates_for_action(self,action):
        '''
        Get all the valid parameters for a given action for the current state of the simulation
        '''
        objects = dict()        
        signatures_to_match = {name:(idx,t) for idx, (name,t) in enumerate(action.signature)}
        index_to_name = {idx:name for idx,name in enumerate(action.signature)}
        candidate_length = len(signatures_to_match)
        found = set()
        candidates = None
        #copy all preconditions
        for precondition in sorted(action.precondition, key=lambda x: len(self.simulator.state[x.name])):
            thruths = self.simulator.state[precondition.name]            
            if len(thruths) == 0: return []
            # map from predicate index to candidate index
            dtypes = [(name,'object') for name in precondition.signature]
            reverse_map = {idx:signatures_to_match[pred][0] for idx,pred in enumerate(precondition.signature)}
            indexes = reverse_map.values()
            overlap = len(found.intersection(indexes)) > 0
            precondition_candidates = []            
            for entry in thruths:
                candidate = [None]*candidate_length
                for idx, param in enumerate(entry):
                    candidate[reverse_map[idx]] = param                    
                precondition_candidates.append(candidate)            
            
            candidates = self.join_candidates(candidates,precondition_candidates,found,indexes)
            # print( candidates)
            found = found.union(indexes)
        
        return [self.indexed_candidate_to_dict(c,index_to_name) for c in candidates]
       

    def get_valid_candidates_for_action_original(self,action):
        '''
        Get all the valid parameters for a given action for the current state of the simulation
        '''
        objects = dict()
        candidates = []
        #copy all preconditions
        precondition_left = action.precondition[:]
        for (name,t) in action.signature:            
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
                # new_candidates[:] = [c for c in new_candidates if precondition.test(c, self.simulator.state)]

            candidates = new_candidates
        return candidates


    
    
   