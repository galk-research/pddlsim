import simulator
from executors import executor


from lapkt.libfdplanner import Planner 

from fd.grounding import encode
import next_actions


class Successors(object):
    def __init__(self, domain_path, problem_path):
        self.task = Planner()
        self.atom_table = next_actions.load( domain_path, problem_path, self.task)
        self.task.setup()
    

    #[['CLEAR', 'A'], ['CLEAR', 'C'], ['CLEAR', 'B'], ['ONTABLE', 'A'], ['ONTABLE', 'B'], ['ONTABLE','D'],['ON', 'C', 'D'],['HANDEMPTY']]
    def expand_simulator_state(self,sim_state):
        return [[predicate_name] + list(pred) for predicate_name,predicate_set in sim_state.items() for pred in predicate_set]
            
                 

    def next(self, sim_state):
        list_state = self.expand_simulator_state(sim_state)
        atoms = next_actions.create_atoms(list_state)
        
        state = self.task.create_state(encode(atoms,self.atom_table))
        return self.task.next_actions(state)
