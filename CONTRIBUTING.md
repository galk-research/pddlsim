
# Structure overview WIP

- domains - a collection of domains used for testing
- lapkt:
    - LAPKT-dev - this is a git submodule contains lapkt source code
    - succ-gen - contains additional source code that is compiled for with LAPKT, this is necessary for successor generation.
    - build_lib.sh - downloads the lapkt source code, build the dependencies for succ_gen and also constructes the liblapkt library
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
- setup.py - run 'python setup.py bdist_wheel' to create a wheel for this library

# Easy reinstall

Run ```./reinstall.sh``` to uninstall the current version of pddlsim, then build a wheel from the current source and install it. This is very useful for testing changes to the library.

# Release

To upload a new version to PyPi:
1. Don't forget to update the version in ```setup.py``` 
2. Build the wheel with ```python setup.py bdist_wheel```
3. Upload the wheel with twine: ```twine upload dist/$(ls dist -t | head -n1)```


