Prerequisites:
    Boost Python - install with ```sudo apt-get install libboost-python-dev```

Installation:
    use ```pip install pddlsim``` to install the library
 
Sample usage:

the following runs a local simulator with a PlanDispatcher executive
```
from pddlsim.local_simulator import LocalSimulator
from pddlsim.executors.plan_dispatch import PlanDispatcher

#domain_path - a path to a pddl file of the domain.
#problem_path - a path to a pddl file of the problem
#PlanDispatcher - an executive that solves the problem with planning.
print LocalSimulator().run(
        domain_path, problem_path, PlanDispatcher())
```

An empty example that shows the necessary functions for an exective can be found in pddlsim/executors/executor.py
All executive must have these 2 functions:
1. initialize(self,services) - called first by the server and recives all the services that are used to communicate with
 the the server. This is where you can initialize anything related to the domain or problem the server is simulating.
2. next_action(self) - returns the next action to execute.

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

Developer notes:

Run ```./reinstall.sh``` to uninstall the current version of pddlsim, then build a wheel from the current source and install it. This is very useful for testing changes to the library.

To upload a new version to PyPi:
1. Don't forget to update the version in ```setup.py``` 
2. Build the wheel with ```python setup.py bdist_wheel```
3. Upload the wheel with twine: ```twine upload dist/$(ls dist -t | head -n1)```


