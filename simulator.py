import pddl.parser

from first_parser import FirstParser

class Simulator(object):
    """docstring for Simulator."""
    def __init__(self, domain_path, print_actions=True):
        super(Simulator, self).__init__()
        self.domain_path = domain_path   
        self.print_actions = print_actions     
        self.reached_goal = False
        self.check_preconditions = True        
     
    

    def apply_action(self, action, params):
        param_mapping = self.parser.get_param_mapping(action,params)
        
        if self.check_preconditions:
            preconditions = self.parser.get_action_preconditions(action)            
            passed = all([self.test_predicate(precondition.name,precondition.signature,param_mapping) for precondition in preconditions])
            if not passed:
                raise PreconditionFalseError()

        for (predicate_name,entry) in self.parser.to_delete(action,param_mapping):
            predicate_set = self.state[predicate_name]
            if entry in predicate_set:
                predicate_set.remove(entry)
        
        for (predicate_name,entry) in self.parser.to_add(action,param_mapping):
            self.state[predicate_name].add(entry)
        
    def act(self, action_sig):
        if self.print_actions:
            print(action_sig)
        
        action_sig = action_sig.strip('()')
        parts = action_sig.split(' ')
        action_name = parts[0]
        param_names = parts[1:]
        
        action = self.parser.get_action(action_name)
        params = [self.parser.get_object(param_name) for param_name in param_names]
        self.apply_action(action, params)

    def simulate(self,problem_path,executor):
        self.problem_path = problem_path
        self.executor = executor
        self.parser = FirstParser(self.domain_path,self.problem_path)
        #setup internal state
        self.state = self.parser.build_first_state()
        self.reached_goal = False
        #setup executor
        self.executor.initilize(self)

        self.action_loop()

    def action_loop(self):
        has_actions = True
        while has_actions:
            action = self.executor.next_action()
            if action:
                self.act(action)
            else:
                has_actions = False
        #check goal
        self.reached_goal = self.check_goal()

    def check_goal(self):
        for (name,signature) in self.parser.get_goals():                        
            if signature not in self.state[name]:
                return False
        return True

    def test_predicate(self, name, signature, dictionary):
        signature = tuple([dictionary[x[0]] for x in signature])
        return signature in self.state[name]

class PreconditionFalseError(Exception):
    pass