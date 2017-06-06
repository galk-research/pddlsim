#! /usr/bin/env python
import sys
import os

from fd.grounding import *
import fd.normalize as normalize
import fd.build_model

from fd.pddl import actions,axioms,conditions, predicates, pddl_types, functions, f_expression
from fd.pddl.tasks import *
import fd.pddl as pddl

from libfdplanner import Planner 
# MRJ: Profiler imports
#from prof import profiler_start, profiler_stop

#copy of fd.grounding.default
def load( domain_file, problem_file, output_task ) :
    # parsing_timer = timers.Timer()
    # print("Domain: %s Problem: %s"%(domain_file, problem_file) )

    task = pddl.open( problem_file, domain_file)
    normalize.normalize(task)

    relaxed_reachable, atoms, actions, axioms, reachable_action_params = explore(task)
    print("goal relaxed reachable: %s" % relaxed_reachable)
    if not relaxed_reachable :
        print("No plan exists")
        sys.exit(2)
    
    print("%d atoms" % len(atoms))

    with timers.timing("Computing fact groups", block=True):
        groups, mutex_groups, translation_key = fact_groups.compute_groups(
            task, atoms, reachable_action_params,
            partial_encoding=USE_PARTIAL_ENCODING)
    
    index = 0
    atom_table = {}

    atom_names = [ atom.text() for atom in atoms ]
    atom_names.sort()
    
    for atom in atom_names :
        atom_table[ atom ] = index
        output_task.add_atom( atom )
        index += 1


    print("Deterministic %d actions" % len(actions))
    nd_actions = {}
    for action in actions :
        #print( "action: %s cost: %d"%(action.name,action.cost) )
        nd_action = PropositionalDetAction( action.name, action.cost )
        nd_action.set_precondition( action.precondition, atom_table )
        nd_action.add_effect( action.add_effects, action.del_effects, atom_table )
        if len(nd_action.negated_conditions) > 0 :
            output_task.notify_negated_conditions( nd_action.negated_conditions )
        nd_actions[ nd_action.name ] = nd_action

    output_task.create_negated_fluents()

    for name, _ in nd_actions.iteritems() :
        output_task.add_action( name )

    index = 0
    for action in nd_actions.values() :
        output_task.add_precondition( index, action.precondition )
        for eff in action.effects :
            output_task.add_effect( index, eff )
        #if len(action.cond_effs) != 0 :
        #	print action.name, len(action.cond_effs), "has conditional effects"
        for cond, eff in action.cond_effs.iteritems() :
            output_task.add_cond_effect( index, list(cond), eff )
        output_task.set_cost( index, action.cost ) 
        index += 1

    # MRJ: Mutex groups processing needs to go after negations are compiled away
    print("Invariants %d"%len(mutex_groups))
    for group in mutex_groups :
        if len(group) >= 2 :
            #print("{%s}" % ", ".join(map(str, group)))
            output_task.add_mutex_group( encode( group, atom_table ) )
            #print( encode( group, atom_table ) )


    output_task.set_domain_name( task.domain_name )
    output_task.set_problem_name( task.task_name )
    output_task.set_init( encode( task.init, atom_table ) )
    output_task.set_goal( encode( task.goal, atom_table ) )
    # output_task.parsing_time = parsing_timer.report()
    return atom_table

def create_atoms(facts):
    initial = []
    initial_true = set()
    initial_false = set()
    initial_assignments = dict()
    for fact in facts:
        fact = map(str.lower,fact)
        if fact[0] == "=":
            try:
                assignment = f_expression.parse_assignment(fact)
            except ValueError as e:
                raise SystemExit("Error in initial state specification\n" +
                                 "Reason: %s." %  e)
            if assignment.fluent in initial_assignments:
                prev = initial_assignments[assignment.fluent]
                if assignment.expression == prev.expression:
                    print("Warning: %s is specified twice" % assignment,
                          "in initial state specification")
                else:
                    raise SystemExit("Error in initial state specification\n" +
                                     "Reason: conflicting assignment for " +
                                     "%s." %  assignment.fluent)
            else:
                initial_assignments[assignment.fluent] = assignment
                initial.append(assignment)
        elif fact[0] == "not":
            atom = conditions.Atom(fact[1][0], fact[1][1:])
            check_atom_consistency(atom, initial_false, initial_true, False)
            initial_false.add(atom)
        else:
            atom = conditions.Atom(fact[0], fact[1:])
            check_atom_consistency(atom, initial_true, initial_false)
            initial_true.add(atom)
    initial.extend(initial_true)
    return initial


def main( domain_file, problem_file, plan_file ) :
    # task = Planner( domain_file, problem_file )
    task = Planner()

    atom_table = load( domain_file, problem_file, task )

    atoms = create_atoms(
        [['CLEAR', 'A'], ['CLEAR', 'C'], ['CLEAR', 'B'], ['ONTABLE', 'A'], ['ONTABLE', 'B'], ['ONTABLE','D'],
                    ['ON', 'C', 'D'],['HANDEMPTY']])
    
    state = task.create_state(encode(atoms,atom_table))
    #MRJ: Uncomment to check what actions are being loaded
    #for i in range( 0, task.num_actions() ) :
    #	task.print_action( i )

    # MRJ: Setting planner parameters is as easy as setting the values
    # of Python object attributes

    # MRJ: log filename set
    task.log_filename = 'iw.log'

    # MRJ: plan file
    task.plan_filename = plan_file

    # MRJ: Comment line below to deactivate profiling
    #profiler_start( 'planner.prof' )

    # MRJ: We call the setup method in SIW_Planner
    task.setup()

    # MRJ: And then we're ready to go
    # task.solve()
    result = task.next_actions(state)
    # print result
    for action in result:
        print action
    #MRJ: Comment lines below to deactivate profile
    #profiler_stop()	

    #rv = os.system( 'google-pprof --pdf libsiw.so siw.prof > siw.pdf' )
    #if rv != 0 :
    #	print >> sys.stderr, "An error occurred while translating google-perftools profiling information into valgrind format"


def debug() :
    main( "domain.pddl", "problem.pddl", "" )

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main( sys.argv[1], sys.argv[2], sys.argv[3] )
    else:
        domain_path,problem_path = 'nav_model_resolution/domain.pddl','nav_model_resolution/corridor_100.pddl'
        main(domain_path,problem_path,'')

