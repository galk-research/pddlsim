Files:

- simulator.py - manages the state of a simulated enviroment
- first_parser.py - handle the specifics of the current pddl parser implementation, current in stages of moving to parser from planning.domains
- planner.py - util for planning, supports using a local planner or an API call
- executor.py - basic prototype for executors, not really used
- plan_dispatch.py - an executor that plans then only executes that plan
- random_executor.py - an executor that executes random valid actions

In progress:

- using the parser from planning.domains, the current parser use python 3 but one from planning.domains uses 2.7. There could be issues because of that

- gathering domains and problem from IPC 2002, then create script for testing all domains and problems. This is to see if the parser and simulator support PDDL 2.1