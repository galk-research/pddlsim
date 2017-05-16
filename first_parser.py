import pddl.parser

class FirstParser(object):    
    def __init__(self,domain_path,problem_path):
        super(FirstParser, self).__init__()
        self.pddlParser = pddl.parser.Parser(domain_path)
        self.domain = self.pddlParser.parse_domain()
        self.pddlParser.set_prob_file(problem_path)
        self.problem = self.pddlParser.parse_problem(self.domain)
    
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
        return self.domain.actions[action_name]
    
    def get_actions(self):
        return self.domain.actions.items()

    def get_param_mapping(self, action, params):
        param_mapping = dict()
        for (name,param_type),obj in zip(action.signature,params):
            param_mapping[name] = obj
        return param_mapping
    
    def get_entry(self, param_mapping, predicate):
        names = [x[0] for x in predicate.signature]
        entry = tuple([param_mapping[name] for name in names])
        return entry
    
    def entries_from_list(self, preds, param_mapping):
        return [(pred.name,self.get_entry(param_mapping,pred)) for pred in preds]

    def to_delete(self, action, param_mapping):
        return self.entries_from_list(action.effect.dellist,param_mapping)        
    
    def to_add(self, action, param_mapping):
        return self.entries_from_list(action.effect.addlist,param_mapping)        
    
    def get_action_string(self, action, dictionary):
        params = " ".join([dictionary[var[0]][0] for var in action.signature])
        return "(" + action.name + " " + params + ")"

    def get_action_preconditions(self, action):
        return action.precondition
    
    def get_action_signature(self, action):
        return [(obj[0],obj[1][0]) for obj in action.signature]

    def has_all_objects(self, precondition,objects):
        return objects.keys() >= {obj_name for (obj_name,t) in precondition.signature}
