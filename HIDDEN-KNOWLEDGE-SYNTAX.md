

The proposed syntax is as close as possible to the existing syntax
for failing actions.

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

We propose to make the hidden knowledge use a similar syntax

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


