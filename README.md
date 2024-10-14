<div align=center>
    <picture>
        <source srcset="/assets/pddlsim-dark.svg" media="(prefers-color-scheme: dark)"/>
        <img alt="PDDLSIM logo" src="/assets/pddlsim-light.svg"/>
    </picture>
    <hr/>
</div>

PDDLSIM is an execution simulator for PDDL[^1] domain-problem pairs, with a supporting library to define agents that interface with said simulator. This can happen locally, or via a remote, internet connection.

PDDLSIM is designed to allow the evaluation of sequential action-selection algorithms across a wide variety of tasks and environments, and was created for the Bar-Ilan University course ["Introduction to Intelligent, Cognitive, and Knowledge-Based Systems" (89-674)](https://www.cs.biu.ac.il/~galk/teach/current/intsys/). In the course, it is used as a part of the final project.

The simulator is run with PDDL[^1] domain and problem files. An agent can then connect to the simulator and interact with it: requesting the domain-problem pair definition, and then attempting to solve the task by selecting actions and sending them to the simulator for execution. The simulator will report the number of actions taken, whether the goal of the task was achieved, the wall-clock time taken, etc. The PDDL description received by the agent may be partially redacted. For example, it might not receive information about action success probabilities, or some objects may remain hidden until the agent reaches a specific state, etc.

## Documentation

The documentation is maintained in the [PDDLSIM wiki](https://github.com/galk-research/pddlsim/wiki). To start, see [Getting Started](https://github.com/galk-research/pddlsim/wiki/Getting-Started). The documentation also includes usage guidelines, information about creating agents that interact with the simulator, and more.

## Installation

PDDLSIM is available on [PyPI](https://pypi.org/project/pddlsim/), requiring no external dependencies. Note that PDDLSIM requires on Python 3.12 or later. Earlier, legacy versions of PDDLSIM are also available on PyPI, but are unsupported, as these use Python 2.7.

To install PDDLSIM using `pip`, run:

```bash
pip install pddlsim
```

Check out [`examples/`](/examples/) for some examples of using PDDLSIM, for creating agents that interface with simulators, running simulators that interface with agents, etc.

## Contributing

For a step-by-step guide to contributing to PDDLSIM, see the [Contributing](https://github.com/galk-research/pddlsim/wiki/Contributing/) page.

[^1]: Some PDDL features, like non-classical planning, are unsupported, and some extensions, such as probabilistic actions, or hidden information, are present.
