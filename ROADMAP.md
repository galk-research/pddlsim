
# Critical issues to be resolved for version 1.0

- Documentation for Architecture in wiki
- "Getting Started" documentation to include two simple runs examples
    - One local, one simulation
- Full "Usage" documentation:
    - Command line flags, if any
    - Different options for choosing planners
    - What are the different sample domains
    - What are the different example executors
    - How to write a new executor
    - How to prevent full problem from being known to user (for instance, so they cannot parse the PDDL to find out where "hidden treasure" is)
    - How to define probabilistic actions


# Consider for next version

- code tests
- pddl Serialization (building blocks complete, just need a full implementation)
- full protocol to manage a simulator with access to a set of problems? (Not really needed, one can run multiple servers, but maybe add code to make running a multi-server easier)
- report cards, and maybe a more general framework for summary statistics
- a more efficient implementation for "get grounded actions" (successor generation) is possible using database theory and query optimization.
  - The gist of it is compiling a precondition into a set of conjunctive queries with negation, and then running these efficiently using join algorithms and filtering for the negations (whenever possible).
  - Good fit for a student interested in these topics.
  - An implementation should probably use FFI. If using Rust, consider Maturin!

