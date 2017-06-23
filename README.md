Files:

- simulator.py - manages the state of a simulated enviroment
- first_parser.py - handle the specifics of the current pddl parser implementation, current in stages of moving to parser from planning.domains
- planner.py - util for planning, supports using a local planner or an API call
- executor.py - basic prototype for executors, not really used
- plan_dispatch.py - an executor that plans then only executes that plan
- random_executor.py - an executor that executes random valid actions

- nav_model_resolution
    - generate_problem.py - tool for generating problems in a maze domain
    - reduce_domain.py - reduces a full maze problem into a simpler problem
    - maze_reducer_executor.py - an executor for maze problems 

Uses a git submodule for including LAPKT. 

To download into the project run the following :
    cd lapkt/LAPKT-dev
    git submodule init
    git submodule update

Next compile libff and libfdplanner.
    change libff make file, add -fPIC to flags