#! /usr/bin/env python
import sys
import os
import random

import liblapkt

def create_and_successors(domain_file, problem_file):
    task = liblapkt.Planner()
    print 'init planner'
    print domain_file, problem_file
    task.load(domain_file,problem_file)
    print 'loaded pddls'
    task.setup()
    sig_to_index = dict()
    for i in range( 0, task.num_actions() ) :
        sig_to_index[task.get_action_signature( i )] = i
    # print sig_to_index

    for _ in range(5):
        print "Applicable actions: "
        result = task.next_actions_from_current()
        for action in result:
            print action,
        random_action = random.choice(result)
        print "picked action: ", random_action
        task.proceed_with_action(sig_to_index[random_action])

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
        main('domain.pddl','corridor_100.pddl','')
