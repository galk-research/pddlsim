from lapkt.libfdplanner import Planner 


from planner_wrapper import Planner_Wrapper


class TrackedSuccessors(object):
    def __init__(self, sim):
        
        # wrapper is used for profiling
        self.task = Planner()        
        self.task.load(sim.domain_path,sim.problem_path)
        self.task.setup()
        self.sig_to_index = dict()
        for i in range( 0, self.task.num_actions() ) :
            self.sig_to_index[self.task.get_action_signature( i )] = i    	
        
        sim.on_action += self.proceed
    
    def next(self):        
        return self.task.next_actions_from_current()

    def proceed(self, action_signature):
        self.task.proceed_with_action(self.sig_to_index[action_signature.upper()])
