<div align=center>
    <picture>
        <source srcset="/assets/pddlsim-dark.svg" media="(prefers-color-scheme: dark)"/>
        <img alt="PDDLSIM logo" src="/assets/pddlsim-light.svg"/>
    </picture>
    <hr/>
</div>

PDDLSIM is an execution simulator for a PDDL domain and problem[^1], with a supporting library to define agents and interface with said simulator, locally, or via a remote connection. The goal of PDDLSIM is to allow evaluating sequential action-selection algorithms across a wide variety of tasks and environments.
PDDLSIM was created for the Bar-Ilan University course ["Introduction to Intelligent, Cognitive, and Knowledge-Based Systems" (89-674)](https://www.cs.biu.ac.il/~galk/teach/current/intsys/), and is used as part of the final project in the course.

The simulator reads a domain description and a task described in PDDL. An agent can connect to the simulator, ask for the domain and task, and then attempt to solve the task by selecting actions to send to the simulator for execution. The simulator reports on number of actions taken, whether the goal of the task was achieved, and the world-time taken. Note that the agent may receive a PDDL description that may be redacted. For example, it might not receive information about action success probabilities, nor objects that remain hidden until the agent reaches a specific state.

For full documentation [see the project wiki](https://bitbucket.org/galk-opensource/executionsimulation/wiki/Home).

For a few example agents, [see the examples folder](./examples) XXX Yoav+Gal discuss

## Installation (Brief)

PDDLSIM is available on [PyPI](https://pypi.org/project/pddlsim/), requiring no external dependencies. Note that PDDLSIM requires Python 3.12 or later. Earlier, legacy versions of PDDLSIM are also available on PyPI, but are unsupported.

To Install, execute: XXX Yoav, fill in command-line

## Documentation

XXX Yoav, note that you are asking the reader to go into the contributor's docs, just so that they can read the user manual. This is not a good idea. I therefore moved everything to a wiki. This section will be deleted after we discuss how to move everything, and why this was a bad idea.

## Documentation for Agent Developers (Agent Builders)

User (agent-builder) documentation is on the [PDDLSIM project wiki](https://bitbucket.org/galk-opensource/executionsimulation/wiki/Home). It includes also brief
overview of example agents.

## Contributing

XXX Yoav: Is this file still needed? >>> 'Please see the [CONTRIBUTING.md](./CONTRIBUTING.md) file for details.'

XXX Yoav: to fix links to wiki, once wiki is fixed.

Content on contribution is available in the documentation, [here](./docs/contributor_guide/). To setup your development environment, see [this](./docs/contributor_guide/setup.rst), and to build the documentation, which requires a development environment, see [this](./docs/contributor_guide/docs.rst).

[^1]: Some PDDL features (non-classical planning) are unsupported, and some extensions are included (action success probabilities, hidden objects).
