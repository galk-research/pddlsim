import pddl.parser
from pddl.pddl import Action as PddlParserAction, Predicate as PddlParserPredicate


class FirstParser(object):    
    def __init__(self,domain_path,problem_path):
        super(FirstParser, self).__init__()
        self.pddlParser = pddl.parser.Parser(domain_path)
        self.domain = self.pddlParser.parse_domain()
        self.pddlParser.set_prob_file(problem_path)
        self.problem = self.pddlParser.parse_problem(self.domain)

        self.actions = {name:Action(action) for name, action in self.domain.actions.items()}
    
    def build_first_state(self):
        initial_state = self.problem.initial_state
        current_state = dict()
        for k,v in self.domain.predicates.items():
            current_state[k] = set()
        for pred in initial_state:
            current_state[pred.name].add(tuple(pred.signature))
        return current_state
    
    def get_object(self,name):
        """ Get a object tuple for a name """
        if name in self.problem.objects:
            return (name,self.problem.objects[name])
        if name in self.domain.constants:
            return (name,self.domain.constants[name])
    
    @staticmethod
    def is_of_type(obj,type):
        if obj is None:
            return False
        if obj == type:
            return True
        return FirstParser.is_of_type(obj.parent,type)

    def get_objects_of_type(self, t):        
        matching_objects = []
        for instance in self.problem.objects.items():
            if self.is_of_type(instance[1], t):
                matching_objects.append(instance)
        return matching_objects


    def get_signature(self,original_signature):
        return tuple([self.get_object(x[0]) for x in original_signature])

    def get_goals(self):
        return [(subgoal.name, self.get_signature(subgoal.signature)) for subgoal in self.problem.goal]

    def get_action(self, action_name):
        # return self.domain.actions[action_name]
        return self.actions[action_name]
        
    @staticmethod
    def get_entry(param_mapping, predicate):
        names = [x[0] for x in predicate.signature]
        entry = tuple([param_mapping[name] for name in names])
        return entry
      

    def has_all_objects(self, precondition, objects):
        return objects.keys() >= {obj_name for (obj_name,t) in precondition.signature}


class Action(object):
    def __init__(self, action):
        self.name = action.name
        self.signature = [(obj[0],obj[1][0]) for obj in action.signature]
        self.effect = action.effect
        self.precondition = list(map(Predicate,action.precondition))

    def action_string(self,dictionary):
        params = " ".join([dictionary[var[0]][0] for var in self.signature])
        return "(" + self.name + " " + params + ")"
    
    def entries_from_list(self, preds, param_mapping):
        return [(pred.name,FirstParser.get_entry(param_mapping,pred)) for pred in preds]

    def to_delete(self, param_mapping):
        return self.entries_from_list(self.effect.dellist,param_mapping)        
    
    def to_add(self, param_mapping):
        return self.entries_from_list(self.effect.addlist,param_mapping)       
    
    def get_param_mapping(self, params):
        param_mapping = dict()
        for (name,param_type),obj in zip(self.signature,params):
            param_mapping[name] = obj
        return param_mapping

class Predicate(object):
    def __init__(self,predicate):
        self.name = predicate.name
        self.signature = predicate.signature
    
    def ground(self, dictionary):
        return tuple([dictionary[x[0]] for x in self.signature])
    
    def test(self, param_mapping, state):        
        return self.ground(param_mapping) in state[self.name]
    