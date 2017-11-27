
import copy
from obsub import event
import time

class Simulator(object):
    """docstring for Simulator."""
    def __init__(self, domain_path, print_actions=True, parser=None):
        super(Simulator, self).__init__()
        self.domain_path = domain_path   
        self.print_actions = print_actions     
        self.reached_goal = False
        self.check_preconditions = True        
        if parser == None:
            # import pddl.parser
            # from first_parser import FirstParser   
            # self.parser_type = FirstParser
            import fd_parser
            self.parser_type = fd_parser.FDParser
        else:
            self.parser_type = parser
     
        
    def apply_action(self, action, params, state=None):    
        if state == None: state = self.state
        param_mapping = action.get_param_mapping(params)
        
        if self.check_preconditions:                        
            for precondition in action.precondition:
                if not precondition.test(param_mapping, state):
                # if not self.test_predicate(precondition.name, precondition.signature, param_mapping):
                    raise PreconditionFalseError()

        for (predicate_name,entry) in action.to_delete(param_mapping):
            predicate_set = state[predicate_name]
            if entry in predicate_set:
                predicate_set.remove(entry)
        
        for (predicate_name,entry) in action.to_add(param_mapping):
            state[predicate_name].add(entry)
        

    def act(self, action_sig, state=None):
        if state == None: state = self.state        
        
        action_sig = action_sig.strip('()').lower()
        parts = action_sig.split(' ')
        action_name = parts[0]
        param_names = parts[1:]
        
        action = self.parser.get_action(action_name)
        params = map(self.parser.get_object,param_names)
        self.apply_action(action, params, state)

    def simulate(self,problem_path,executor):
        self.problem_path = problem_path
        self.executor = executor
        
        self.parser = self.parser_type(self.domain_path,self.problem_path)
        
        #setup internal state
        self.state = self.parser.build_first_state()
        self.reached_goal = False

        t0 = time.time()
        #setup executor
        self.executor.initilize(self)
        if self.print_actions:
            def printer(self,text):
                print text
            self.on_action += printer

        self.action_loop()
        self.reached_goal = self.check_goal()

        t1 = time.time()        
        return t1-t0
    
    @event
    def on_action(self,action_sig):
        pass

    def action_loop(self):
        has_actions = True
        while has_actions:
            action = self.executor.next_action()
            if action:                
                action = action.lower()
                self.act(action)                
                self.on_action(action)
            else:
                has_actions = False        

    


    def check_goal(self):
        for (name,signature) in self.parser.get_goals():                        
            if signature not in self.state[name]:
                return False
        return True

    def test_predicate(self, name, signature, dictionary):
        signature = tuple([dictionary[x[0]] for x in signature])
        return signature in self.state[name]

    def clone_state(self):
        return {name:set(entries) for name, entries in self.state.items()}

    def generate_problem(self,path):
        '''
        generate a pddl problem at the path
        this problem will be from the current state and not the original state
        '''
        predicates = [("(%s %s)"%(predicate_name," ".join(map(str,pred)))) for predicate_name,predicate_set in self.state.iteritems() for pred in predicate_set if predicate_name != '=']
        self.parser.generate_problem(path, predicates)
        return path


class PreconditionFalseError(Exception):
    pass

def compare_executors(domain_path,problem_path, executors):
    results = dict()    
    for name, executor in executors.items():        
        
        sim = Simulator(domain_path,print_actions=False)
        total = sim.simulate(problem_path, executor)
        # print(name, total)
        results[name] = total
    return results