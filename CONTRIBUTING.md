
# Structure overview
- docs/ - auto generated docs
- domains/ - a collection of domains used for testing
- lapkt/ - pddlsim uses a modified version of LAPKT for efficent successor generation
    - LAPKT-dev/ - this is a git submodule contains lapkt source code
    - succ-gen/ - contains additional source code that is compiled for with LAPKT, this is necessary for successor generation.
    - build_lib.sh - downloads the lapkt source code, build the dependencies for succ_gen and also constructes the liblapkt library
- pddlsim/ - this is what you get when you install the package
    - executors/ - some executives you can use or extend
    - external/ - code used from other sources:
          - the compiled lapkt library
          - fd parser (also copied from LAPKT)
          - siw-then-bfsf planner (from planning.domains)
    - remote/ - package for using sockets to run a simulator server and executive client, we use this to better profile executive only performance
    - services/ - api's that the simulator manages and that executive can use, this includes generating sub-problems, perception, tracking goals, and querying for valid actions
    - fd_parser.py - wrapper around fd_parser to convert to format used in simulator
    - local_simulator.py - use this to run a non-remote simulator 
    - parser_independent.py - this is the abstraction used in the simulator, 
    - planner.py - util for planning, supports using a local planner or an API call
    - simulator.py - base simulator - used by both local and remote simulators
- tests/ - a set of test to ensure everything is working, use pytest to run them
- tools/ - some useful tools for generating problems or running a remote server
- setup.py - run 'python setup.py bdist_wheel' to create a wheel for this library

# Easy reinstall

Run ```./reinstall.sh``` to uninstall the current version of pddlsim, then build a wheel from the current source and install it. This is very useful for testing changes to the library.

# Release

To upload a new version to PyPi:
1. Don't forget to update the version in ```setup.py``` 
2. Build the wheel with ```python setup.py bdist_wheel```
3. Upload the wheel with twine: ```twine upload dist/$(ls dist -t | head -n1)```


