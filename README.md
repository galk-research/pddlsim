use ```pip install pddlsim``` to install the library
 
sample usage of the library:
```
from pddlsim.local_simulator import LocalSimulator
from pddlsim.executors.plan_dispatch import PlanDispatcher

print LocalSimulator().run(
        domain_path, problem_path, PlanDispatcher())
```
This code should use a plan dispatcher to solve the problem 

An empty example that shows the necessary functions for an exective can be found in pddlsim/executors/executor.py


Project structure:

- dist - contains distributions of this project, created using setuptools (see setup.py)
- domains - a small collection of domains used for testing
- lapkt:
    - LAPKT-dev - this is a git submodule contains lapkt source code
    - succ-gen - contains additional source code that is compiled for with LAPKT, this is necessary for successor generation.
    - build_lib.sh - downloads the lapkt source code, build the dependencies for succ_gen and also constructes the liblapkt library
- experiments - code used for a experiments, includes code to generate a few some problems with variable sizes
    - generate_problem.py - tool for generating problems in a maze domain
    - reduce_domain.py - reduces a full maze problem into a simpler problem
    - maze_reducer_executor.py - an executor for maze problems 
- pddlsim - this is the primary directory of this library, the files in here are what sould be distributed to users of this library
    - executors - sample executives
    - external - code used from other sources:
          - the compiled lapkt library
          - fd parser (also copied from LAPKT)
          - siw-then-bfsf planner (from planning.domains)
    - simulator.py - manages the state of a simulated enviroment
    - first_parser.py - handle the specifics of the current pddl parser implementation, current in stages of moving to parser from planning.domains
    - planner.py - util for planning, supports using a local planner or an API call
    - executor.py - basic prototype for executors, not really used
    - plan_dispatch.py - an executor that plans then only executes that plan
    - random_executor.py - an executor that executes random valid actions
- main.py  - used to run experiments  
- setup.py - run 'python setup.py bdist_wheel' to create a wheel for this library
