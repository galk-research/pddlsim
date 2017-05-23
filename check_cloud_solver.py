from cloud_solver.utils.parser import Problem
import os
import glob
import planner

# domain_path,problem_path = 'domains/Log_dom.pddl','domains/Log_ins.pddl'
# domain_path,problem_path = 'domains/Mapana_dom.pddl','domains/Mapana_ins.pddl'
# domain_path,problem_path = 'domains/Sched_dom.pddl','domains/Sched_ins.pddl'
# domain_path,problem_path = 'domains/Elev_dom.pddl','domains/Elev_ins.pddl'

problems = []
for problem_path in glob.glob('ipc2002/*/prob*.pddl'):
    domain_path = os.path.join(os.path.dirname(problem_path),'domain.pddl')
    # problems.append((domain_path,problem_path))
    planner.local(domain_path,problem_path)
# task = Problem(domain_path, problem_path)
# print task
