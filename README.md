 # Intro
This project allows you to simulate an environment defined with the PDDL syntax. You can then run executors in these environment and attempt to solve their different problems.

The executor won't necessarily be seeing the same PDDL as supplied to the simulator. This allows all sorts of modifications to the environment, for example, some things could be revealed only in certain situations. The executor shouldn't know of this beforehand.

## Prerequisites:
Boost Python - install with ```sudo apt-get install libboost-python-dev```

# Installation

run ```pip install pddlsim``` to install the library

using the planner requires a UNIX based operating system.
this also means that using the planner and planning based executives won't work on Windows

# Running an executive
For quickly prototyping it is simplest to test things with the LocalSimulator:   
```
#!python
from pddlsim.local_simulator import LocalSimulator
from pddlsim.executors.random_executor import RandomExecutor

domain = # path to a domain
problem = # path to a problem in that domain
executor = RandomExecutor()

report = LocalSimulator().run(domain, problem, executor)
print report
```
here is an example output:
```
== REPORT CARD ==
Success: True

Start time: 1583491991.49
End time: 1583491991.5
Total time: 0.00799989700317

Total actions: 6
Total actions costs: 6
Failed actions: 0
Total perception requests: 7
```


# Building your own executor
Here is an example of an executor, that prefers actions that will immediately reach a goal:
```
#!python
import random

class MyExecutor(object):
    def __init__(self, option_a=1):
        # use the constructor to configure the executor
        self.optionA = option_a
    
    def initialize(self, services):
        # the services are a set of tools that allow you understand the state of the world 
        # in this case we are keeping a reference to them, so that they can be accessed later
        self.services = services
    
    def next_action(self):
        # this is the core of the executor, here you must return the next action to apply
        if self.services.goal_tracking.reached_all_goals():
            # here we use the goal_tracking service, to test if we reached the goals
            # None is used indicate that the goal has been reached 
            return None
        
        # the valid options services gives the actions that can be applied
        options = self.services.valid_actions.get()
        # the perception services gives the current state
        current_state = self.services.perception.get_state()

        # go through all the valid action and look for one that will complete a goal
        for option in options:
            # the parser services provides method for examining or modifying the pddl syntax
            new_state_from_option = self.services.parser.copy_state(current_state)
            self.services.parser.apply_action_to_state(option, new_state_from_option, check_preconditions=False)
            # here we use the goal tracking services to check all uncompleted goals
            for goal in self.services.goal_tracking.uncompleted_goals:
                if self.services.parser.test_condition(
                    goal, new_state_from_option):
                    return option
        # if none were found, then pick an option at random
        return random.choice(options)
```

We can then test our new executor like this:
```
from pddlsim.local_simulator import LocalSimulator

print LocalSimulator().run(domain, problem, MyExecutor())
```

# Services
## goal_tracking
keeps track of which goals were complete and are still incomplete
- ```reached_all_goals()``` - have all goals been reached
- ```uncompleted_goals``` - a list of uncompleted goals

## parser
holds a copy of the parser used for understanding the pddl format.
also has methods for modifying state and testing conditions
- ```test_condition(condition, state)``` - goals are a type of condition
- ```apply_action_to_state(action, state, check_preconditions)``` - modifies the state with the affect of the action
## pddl
- ```domain_path``` - path to domain pddl file
- ```problem_path``` - path to problem pddl file

## perception
- ```get_state()``` - gets a copy of the current state, this isn't necessary the true state of the environment

## valid_action
- ```get()``` - returns a list of valid actions from the current state. there is a very efficent version of this that requires tracking, but it doesn't work on all system. A slower fallback written in python is provided for those cases

# Client Server separation
In order to separate between the executor and the environment more clearly. It is possible to run them separately and then have them communicate using sockets. This means that they can also be on separate computer. With this profiling resources used by the executor is simpler.

## To run the server:
```
#!python
from pddlsim.remote.simulator_server import SimulatorForkedTCPServer

domain = # path to domain
problem = # path to problem

server = SimulatorForkedTCPServer.default()
server.provide_pddls(domain, problem).serve_forever()
```

## To run an executor using this server:
This should be run as a separate instance 
```
#!python
from pddlsim.executors.random_executor import RandomExecutor
from pddlsim.remote.remote_simulator import RemoteSimulator

# these are the default host and ports:
HOST, PORT = "localhost", 9999

# this is the executive we want to use
executive = RandomExecutor()

with RemoteSimulator(HOST, PORT) as sim:
    result = sim.simulate(executive)
print result
```

For a more complete example, including profiling see:
- ```tools\profile_on_remote_client.py```
- ```tools\profile_on_remote_server.py```


# Additional Syntax

## Fail-able actions syntax
To represent actions that fail, we currently use the following syntax
in a problem domain file (for example problem.pddl):
```
    (:fails ((at person1 t2) (move-east) 0.9))
```
The idea here is that the simulator knows to watch for the predicate
`(at person1 t2)` in the current state. When it is true, then *if*
the agent chooses the action `(move-east)` (with any parameters), then
the action will fail with probability 0.9, meaning that the state
will not change.

## Probabilistic effects syntax
Probabilistic effects are an expansion on failable effects.
They allow you to specify a different effect instead of just failing:
```
(:action move-south
 :parameters ( ?p ?a ?b ?c)
 :precondition
	(and (person ?p) (empty ?b) (at ?p ?a)  (south ?a ?b) (north ?a ?c) (empty ?c))
 :effect
    (probabilistic  0.75 (and (at ?p ?b) (not (at ?p ?a)))
                    0.25 (and (at ?p ?c) (not (at ?p ?a))))
```
## Hidden Knowledge Syntax

The syntax is as close as possible to the existing syntax
for failing actions.
```
   (:reveal ((at person1 t2) (and (at food t3) (at sword t2) 0.9)))
```

Which would mean the following:
  if the simulator determines that `(at person1 t2)` is true in the
  current state, then when asked for perception, then with probability
  0.9 (i.e., 9 out of 10 times), it will add the following predicates 
  to the state sent to the agent:
  `(at food t3)`
  `(at sword t2)`

 IMPORTANT
 1.  The condition (e.g., (at person t2)) may also be complex (i.e., use and/or)
 2.  The information is revealed only if the condition holds. Once it no longer
     holds, then the information is not sent any more. It would be up to a smart
     agent to remember.
 3.  The is free to act on the information when it is revealed, and only then.
     So, assuming we have an action '(pick-food)', it *will* work and be
     applicable if `(at person1 t2)`, and will *not* work otherwise.
 4.  For this reason, and for others, the predicates that are revealed will **not**
     be listed in the `:init` section of the problem pddl, but only in the `:reveal` clauses.


