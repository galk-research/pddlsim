import lapkt.fd.pddl as pddl
# from pddl.pddl import Action as PddlParserAction, Predicate as PddlParserPredicate
from six import iteritems,print_

class FDParser(object):    
    def __init__(self,domain_path,problem_path):
        super(FDParser, self).__init__()
        self.task  = pddl.pddl_file.open(problem_path, domain_path)        
        self.objects = {obj.name:obj.type for obj in self.task.objects}
        self.actions = {action.name:Action(action) for action in self.task.actions}
    
    def build_first_state(self):
        initial_state = self.task.init
        current_state = dict()
        for predicate in self.task.predicates:
            current_state[predicate.name] = set()
        for atom in initial_state:
            current_state[atom.key[0]].add(atom.key[1])
        return current_state
    
    def get_object(self,name):
        """ Get a object tuple for a name """
        if name in self.objects:
            return (name,self.objects[name])
        # if name in self.task.constants:
        #     return (name,self.domain.constants[name])
    
    # @staticmethod
    # def is_of_type(obj,type):
    #     if obj is None:
    #         return False
    #     if obj == type:
    #         return True
    #     return FDParser.is_of_type(obj.parent,type)

    # def get_objects_of_type(self, t):        
    #     matching_objects = []
    #     for instance in self.problem.objects.items():
    #         if self.is_of_type(instance[1], t):
    #             matching_objects.append(instance)
    #     return matching_objects


    def get_signature(self,original_signature):
        return tuple([self.get_object(x[0]) for x in original_signature])
    
    # currently only support conjunctions
    def get_goals(self):
        return [subgoal.key for subgoal in self.task.goal.parts]

    def get_action(self, action_name):
        # return self.domain.actions[action_name]
        return self.actions[action_name]
        
    @staticmethod
    def get_entry(param_mapping, predicate):
        names = [x for x in predicate]
        entry = tuple([param_mapping[name][0] for name in names])
        return entry
      

    # def has_all_objects(self, precondition, objects):
    #     return objects.keys() >= {obj_name for (obj_name,t) in precondition.signature}


class Action(object):
    def __init__(self, action):
        self.name = action.name
        self.signature = [(obj.name,obj.type) for obj in action.parameters]
        self.addlist = []
        self.dellist = []
        for effect in action.effects:
            if effect.literal.negated:
                self.dellist.append(effect.literal.key)
            else:
                self.addlist.append(effect.literal.key)
        self.precondition = [Predicate.from_predicate(pred) for pred in action.precondition.parts]

    def action_string(self,dictionary):
        params = " ".join([dictionary[var[0]] for var in self.signature])
        return "(" + self.name + " " + params + ")"
    
    def entries_from_list(self, preds, param_mapping):
        return [(pred[0],FDParser.get_entry(param_mapping,pred[1])) for pred in preds]

    def to_delete(self, param_mapping):
        return self.entries_from_list(self.dellist,param_mapping)
    
    def to_add(self, param_mapping):
        return self.entries_from_list(self.addlist,param_mapping)       
    
    def get_param_mapping(self, params):
        param_mapping = dict()
        for (name,param_type),obj in zip(self.signature,params):
            param_mapping[name] = obj
        return param_mapping

class Predicate(object):
    def __init__(self, name, signature):
        self.name = name
        self.signature = signature  
   
    @staticmethod
    def from_predicate(predicate):
        return Predicate(predicate.predicate,predicate.args)

    def ground(self, dictionary):
        return tuple([dictionary[x][0] for x in self.signature])
    
    def test(self, param_mapping, state):        
        return self.ground(param_mapping) in state[self.name]


def main():
    domain_path, problem_path = "ipc2002/zenotravel/domain.pddl","ipc2002/zenotravel/prob01.pddl"
    # parser = FDParser(domain_path, problem_path)
    # print(parser.build_first_state())
    # print(parser.get_object('city1'))
    # print(parser.get_goals())

    import simulator
    from executors.executor import Executor
    from executors.plan_dispatch import PlanDispatcher
    from executors.random_executor import RandomExecutor
    sim = simulator.Simulator(domain_path,parser=FDParser)
    sim.simulate(problem_path,RandomExecutor())
    

if __name__ == '__main__':
    main()