# Prerequisites:
    Boost Python - install with ```sudo apt-get install libboost-python-dev```

# Installation:
    use ```pip install pddlsim``` to install the library
 
# Sample usage:

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

# Supported formats
see tests for examples on:
- Failable action
- PPDDL - probablistic PDDL
- Hidden Knowledge
