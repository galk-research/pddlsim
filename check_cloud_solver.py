from cloud_solver.utils.parser import Problem

# domain_path,problem_path = 'domains/Log_dom.pddl','domains/Log_ins.pddl'
domain_path,problem_path = 'domains/Mapana_dom.pddl','domains/Mapana_ins.pddl'
# domain_path,problem_path = 'domains/Sched_dom.pddl','domains/Sched_ins.pddl'
# domain_path,problem_path = 'domains/Elev_dom.pddl','domains/Elev_ins.pddl'
task = Problem(domain_path, problem_path)
print task
