<div align=center>
    <img alt="PDDLSIM logo" src="./docs/_static/pddlsim-light.svg"/>
    <hr/>
</div>

PDDLSIM is a simulator for a PPDDL-like language[^1] [^2], with a supporting library to define agents and interface with said simulator, locally, or via a remote connection. PDDLSIM was created for the Bar-Ilan University course ["Introduction to Intelligent, Cognitive, and Knowledge-Based Systems" (89-674)](https://u.cs.biu.ac.il/~kaminkg/teach/current/intsys/).

## Installation

PDDLSIM is available on [PyPI](https://pypi.org/project/pddlsim/), requiring no external dependencies. Note that PDDLSIM requires on Python 3.12 or later. Earlier, legacy versions of PDDLSIM are also available on PyPI, but are unsupported.

## Documentation

The documentation, in RST, is available [here](./docs/) folder. To manually build the documentation, see the "Contriburing - Building the documentation" section below. In the future, the documentation will be available online.

## Contributing

Content on contribution is available in the documentation, [here](./docs/contributor_guide/). To setup your development environment, see [this](./docs/contributor_guide/setup.rst), and to build the documentation, which requires a development environment, see [this](./docs/contributor_guide/docs.rst).


[^1]: This is despite the fact the project is named **PDDL**SIM and not **PPDDL**SIM.
[^2]: Some PDDL features, like those not featured in classical planning, are unsupported, and some extensions are present.
