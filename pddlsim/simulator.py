
import copy
from obsub import event
import time
from services.simulator_mediator import SimulatorMediator
from services.goal_tracking import GoalTracking
from services.perception import Perception
from fd_parser import PreconditionFalseError

class Simulator(object):
    """docstring for Simulator."""
    def __init__(self, domain_path, print_actions=True, parser=None):
        super(Simulator, self).__init__()
        self.domain_path = domain_path
        self.print_actions = print_actions
        self.check_preconditions = True
        self.goal_tracking = None        
        self.report_card = None

        if parser is None:
            import fd_parser
            self.parser_type = fd_parser.FDParser
        else:
            self.parser_type = parser


    def simulate(self, problem_path, executor):
        init = lambda : executor.initilize(SimulatorMediator(self))
        return self.simulate_with_funcs(problem_path, init, executor.next_action)

    def simulate_with_funcs(self,problem_path,init_func,next_action_func):
        self.problem_path = problem_path

        self.parser = self.parser_type(self.domain_path,self.problem_path)
        #setup internal state
        self._state = self.parser.build_first_state()

        self.goal_tracking = GoalTracking(self.parser,lambda : self._state)
        self.on_action +=  lambda s,sim: self.goal_tracking.on_action()

        self.report_card = ReportCard().start()
        
        #setup executor
        init_func()
        
        if self.print_actions:
            def printer(self,text):
                print text
            self.on_action += printer        

        self.action_loop(next_action_func)
        
        return self.report_card.done(self.goal_tracking.reached_all_goals())

    @event
    def on_action(self,action_sig):
        pass

    def action_loop(self, next_action_func):
        while True:
            action = next_action_func()
            if not action or action.lower() == '(reach-goal)':
                return
            try:
                self.parser.apply_action_to_state(action,self._state,self.check_preconditions)
                self.on_action(action)
                self.report_card.add_action()
            except PreconditionFalseError as e:
                self.report_card.add_action(True)
            
    def perceive_state(self):
        self.report_card.add_perception()
        return {name:set(entries) for name, entries in self._state.items()}

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
    

def compare_executors(domain_path, problem_path, executors):
    results = dict()
    for name, executor in executors.items():
        sim = Simulator(domain_path,print_actions=False)
        total = sim.simulate(problem_path, executor)
        # print(name, total)
        results[name] = total
    return results
