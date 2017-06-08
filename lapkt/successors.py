import simulator
from executors import executor


from lapkt.libfdplanner import Planner 

from fd.grounding import encode
import next_actions

from planner_wrapper import Planner_Wrapper
from lapkt.fd.pddl.conditions import Atom

class Successors(object):
    def __init__(self, domain_path, problem_path):
        use_wrapper = True
        if use_wrapper:
            self.task = Planner_Wrapper()            
        else:
            self.task = Planner()
        self.atom_table = next_actions.load( domain_path, problem_path, self.task.task if use_wrapper else self.task)
        self.task.setup()
    
    
    
    #[['CLEAR', 'A'], ['CLEAR', 'C'], ['CLEAR', 'B'], ['ONTABLE', 'A'], ['ONTABLE', 'B'], ['ONTABLE','D'],['ON', 'C', 'D'],['HANDEMPTY']]
    def expand_simulator_state(self,sim_state):
        return [[predicate_name] + list(pred) for predicate_name,predicate_set in sim_state.items() for pred in predicate_set if predicate_name != '=']
            
    def create_atoms(self,sim_state):             
        return [Atom(predicate_name,list(pred)) for predicate_name,predicate_set in sim_state.items() for pred in predicate_set if predicate_name != '=']
        
    def next(self, sim_state):
        # list_state = self.expand_simulator_state(sim_state)
        # atoms = next_actions.create_atoms(list_state)
        
        atoms = self.create_atoms(sim_state)
        state = self.task.create_state(encode(atoms,self.atom_table))
        return self.task.next_actions(state)
