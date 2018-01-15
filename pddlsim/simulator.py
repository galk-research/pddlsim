
import copy
from obsub import event
import time
from services.simulator_mediator import SimulatorMediator

class Simulator(object):
    """docstring for Simulator."""
    def __init__(self, domain_path, print_actions=True, parser=None):
        super(Simulator, self).__init__()
        self.domain_path = domain_path
        self.print_actions = print_actions
        self.check_preconditions = True
        self.completed_goals = []
        self.uncompleted_goals = []
        self.dirty = True
        self.report_card = None

        if parser == None:
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
                    raise PreconditionFalseError()

        for (predicate_name,entry) in action.to_delete(param_mapping):
            predicate_set = state[predicate_name]
            if entry in predicate_set:
                predicate_set.remove(entry)

        for (predicate_name,entry) in action.to_add(param_mapping):
            state[predicate_name].add(entry)

        self.dirty = True


    def act(self, action_sig, state=None):
        if state == None: state = self.state

        action_sig = action_sig.strip('()').lower()
        parts = action_sig.split(' ')
        action_name = parts[0]
        param_names = parts[1:]

        action = self.parser.get_action(action_name)
        params = map(self.parser.get_object,param_names)        
        self.apply_action(action, params, state)

    def simulate(self, problem_path, executor):
        init = lambda : executor.initilize(SimulatorMediator(self))
        return self.simulate_with_funcs(problem_path, init, executor.next_action)

    def simulate_with_funcs(self,problem_path,init_func,next_action_func):
        self.problem_path = problem_path

        self.parser = self.parser_type(self.domain_path,self.problem_path)

        #setup internal state
        self.state = self.parser.build_first_state()
        self.completed_goals = []
        self.uncompleted_goals = self.parser.get_goals()[:]

        self.report_card = ReportCard().start()
        #setup executor
        init_func()
        if self.print_actions:
            def printer(self,text):
                print text
            self.on_action += printer

        self.action_loop(next_action_func)
        
        return self.report_card.done(self.reached_all_goals)

    @event
    def on_action(self,action_sig):
        pass

    def action_loop(self, next_action_func):
        while True:
            action = next_action_func()
            if not action or action.lower() == '(reach-goal)':
                return
            try:
                self.act(action)    
                self.on_action(action)
                self.report_card.add_action()
            except PreconditionFalseError as e:
                self.report_card.add_action(True)
            

    @property
    def reached_all_goals(self):
        if self.dirty:
            self.check_goal()
            self.dirty = False
        return not self.uncompleted_goals

    def check_goal(self):
        to_remove = list()
        for goal in self.uncompleted_goals:
                # done_subgoal = all(signature in self.state[name] for (name,signature) in goal )
                done_subgoal = self.parser.test_condition(goal,self.state)
                if done_subgoal:
                    to_remove.append(goal)
        for goal in to_remove:
            self.uncompleted_goals.remove(goal)
            self.completed_goals.append(goal)
        # return self.reached_all_goals

    def clone_state(self):
        return {name:set(entries) for name, entries in self.state.items()}

    def generate_problem(self, path, goal = None):
        """
        generate a pddl problem at the path
        this problem will be from the current state and not the original state
        """
        if goal is None:
            goal = self.uncompleted_goals[0]
        self.parser.generate_problem(path, self.state, goal)
        return path

class ReportCard():
    def __init__(self):
        self.success = False
        self.failed_actions = 0        
        self.total_perception_requests = 0
        self.total_actions = 0
        self.total_action_costs = 0
        self.start_time = None
        self.end_time = None
        self.total_time = None
    
    def add_perception(self):
        self.total_perception_requests += 1

    def add_action(self, failed=False, cost=1):
        self.total_actions += 1
        if failed:
            self.failed_actions += 1
        else:
            self.total_action_costs += cost
    
    def start(self):
        """ 
        Record start time
        :return: self for a fluent api
        """
        self.start_time = time.time()
        return self
    
    def done(self, success):
        """
        Record end time and success
        :return: self for a fluent api
        """
        self.end_time = time.time()
        self.total_time = self.end_time - self.start_time
        self.success = success
        return self
    
    def __str__(self):
        """
        Print the report card in a nice format
        """
        return """
== REPORT CARD ==
Success: {0.success}

Start time: {0.start_time}
End time: {0.end_time}
Total time: {0.total_time}

Total actions: {0.total_actions}
Total actions costs: {0.total_action_costs}
Failed actions: {0.failed_actions}
Total perception requests: {0.total_perception_requests}""".format(self)
    

class PreconditionFalseError(Exception):
    pass

def compare_executors(domain_path, problem_path, executors):
    results = dict()
    for name, executor in executors.items():
        sim = Simulator(domain_path,print_actions=False)
        total = sim.simulate(problem_path, executor)
        # print(name, total)
        results[name] = total
    return results
