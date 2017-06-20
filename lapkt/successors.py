from lapkt.libfdplanner import Planner 

from fd.grounding import encode
from lapkt.fd.pddl.conditions import Atom

import lapkt.fd.pddl as pddl

import next_actions

from planner_wrapper import Planner_Wrapper


class Successors(object):
    def __init__(self, domain_path, problem_path):
        # wrapper is used for profiling
        use_wrapper = True
        if use_wrapper:
            self.task = Planner_Wrapper()            
        else:
            self.task = Planner()
        # next_actions.load is fd.grounding.default that returns the atom_table
        self.atom_table = next_actions.load( domain_path, problem_path, self.task.task if use_wrapper else self.task)
        self.task.setup()
     
    def create_atoms(self,sim_state):             
        return [("%s_%s"%(predicate_name,"_".join(map(str,pred))),False) for predicate_name,predicate_set in sim_state.items() for pred in predicate_set if predicate_name != '=']

    def next(self, sim_state):        
        atoms = self.create_atoms(sim_state)
        # encoded = encode(atoms,self.atom_table)
        # state = self.task.create_state(encoded)
        return self.task.next_actions_from_atoms(atoms,self.atom_table)
        # return self.task.next_actions(state)
    
    def next_from_current(self):
        return self.task.next_actions_from_current()
