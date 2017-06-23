#! /usr/bin/env python
import sys
import os

# add fd parser to path
sys.path.append(os.path.join(os.getcwd(),'lapkt/LAPKT-dev/external'))


import random
from fd.grounding import *
import fd.normalize as normalize
import fd.build_model

from fd.pddl import actions,axioms,conditions, predicates, pddl_types, functions, f_expression
from fd.pddl.tasks import *
import fd.pddl as pddl
from fd.pddl.conditions import Atom


# MRJ: Profiler imports
#from prof import profiler_start, profiler_stop

#copy of fd.grounding.default
# def load( domain_file, problem_file, output_task ) :
#     # parsing_timer = timers.Timer()
#     # print("Domain: %s Problem: %s"%(domain_file, problem_file) )

#     task = pddl.open( problem_file, domain_file)
#     normalize.normalize(task)

#     relaxed_reachable, atoms, actions, axioms, reachable_action_params = explore(task)
#     print("goal relaxed reachable: %s" % relaxed_reachable)
#     if not relaxed_reachable :
#         print("No plan exists")
#         sys.exit(2)
    
#     print("%d atoms" % len(atoms))

#     with timers.timing("Computing fact groups", block=True):
#         groups, mutex_groups, translation_key = fact_groups.compute_groups(
#             task, atoms, reachable_action_params,
#             partial_encoding=USE_PARTIAL_ENCODING)
    
#     index = 0
#     atom_table = {}

#     atom_names = [ atom.text() for atom in atoms ]
#     atom_names.sort()
    
#     for atom in atom_names :
#         atom_table[ atom ] = index
#         output_task.add_atom( atom )
#         index += 1


#     print("Deterministic %d actions" % len(actions))
#     nd_actions = {}
#     for action in actions :
#         #print( "action: %s cost: %d"%(action.name,action.cost) )
#         nd_action = PropositionalDetAction( action.name, action.cost )
#         nd_action.set_precondition( action.precondition, atom_table )
#         nd_action.add_effect( action.add_effects, action.del_effects, atom_table )
#         if len(nd_action.negated_conditions) > 0 :
#             output_task.notify_negated_conditions( nd_action.negated_conditions )
#         nd_actions[ nd_action.name ] = nd_action

#     output_task.create_negated_fluents()

#     for name, _ in nd_actions.iteritems() :
#         output_task.add_action( name )

#     index = 0
#     for action in nd_actions.values() :
#         output_task.add_precondition( index, action.precondition )
#         for eff in action.effects :
#             output_task.add_effect( index, eff )
#         #if len(action.cond_effs) != 0 :
#         #	print action.name, len(action.cond_effs), "has conditional effects"
#         for cond, eff in action.cond_effs.iteritems() :
#             output_task.add_cond_effect( index, list(cond), eff )
#         output_task.set_cost( index, action.cost ) 
#         index += 1

#     # MRJ: Mutex groups processing needs to go after negations are compiled away
#     print("Invariants %d"%len(mutex_groups))
#     for group in mutex_groups :
#         if len(group) >= 2 :
#             #print("{%s}" % ", ".join(map(str, group)))
#             output_task.add_mutex_group( encode( group, atom_table ) )
#             #print( encode( group, atom_table ) )


#     output_task.set_domain_name( task.domain_name )
#     output_task.set_problem_name( task.task_name )
#     output_task.set_init( encode( task.init, atom_table ) )
#     output_task.set_goal( encode( task.goal, atom_table ) )
#     # output_task.parsing_time = parsing_timer.report()
#     return atom_table


# def create_atoms(state):             
#         return [Atom(pred[0].lower(),map(str.lower,pred[1:]))  for pred in state]

import libfdplanner 
def create_and_successors(domain_file, problem_file):
    reload(libfdplanner)    
    task = libfdplanner.Planner()
    print 'init planner'
    print domain_file, problem_file    
    task.load(domain_file,problem_file)        
    print 'loaded pddls'
    task.setup()
    sig_to_index = dict()
    for i in range( 0, task.num_actions() ) :
        sig_to_index[task.get_action_signature( i )] = i    	
    print sig_to_index
    
    
    for _ in range(5):
        print "Applicable actions: "
        result = task.next_actions_from_current()
        for action in result:
            print action,
        random_action = random.choice(result)
        print "picked action: ", random_action
        task.proceed_with_action(sig_to_index[random_action])
    
    # del libfdplanner from Planner

def main( domain_file, problem_file, plan_file ) :
    for _ in range(2):
        create_and_successors(domain_file,problem_file)


def debug() :
    main( "domain.pddl", "problem.pddl", "" )

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main( sys.argv[1], sys.argv[2], sys.argv[3] )
    else:
        main('domain-blocksaips.pddl','blocksaips03.pddl','')

