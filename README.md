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

PDDLSIM uses [PDM](https://pdm-project.org) as its build tool and dependency manager. To work on PDDLSIM, it is recommended, but not strictly required you use it, while developing PDDLSIM. PDM is PDDLSIM's build backend, and is additionally used to specify development dependencies (via `tool.pdm.dev-dependencies`), that need to be installed for performing various development related tasks, e.g. running tests utilizing `pytest` (and some extra plugins), building the documentation using Sphinx (and the required theme and extensions), etc.

### Developing with PDM

To use PDM with the project, first install PDM. See [this](https://pdm-project.org/latest/#installation) for more information on installation. Once you have PDM installed run:

```bash
pdm use
```

And select a base interpreter, to configure a Virtual Environment for development. Then, get the command for activating the Virtual Environment with:

```bash
pdm venv activate
```

And run the command. You will now be inside the Virtual Environment, which is currently _empty_. To install _all_ of PDDLSIM's dependencies, _including development-related_ ones, such that PDDLSIM is in editable mode, run:

```bash
pdm install
```

To _avoid_ installing development dependencies, add the `--production` flag. Additionally, you can prevent any local package being installed in editable mode by using the `--no-editable` flag. Other options are by using the `--help` flag. 

At this stage, you should be able to begin development with no issue. Make sure to the newly created Python interpreter to your code editor. Its path can be found in the `.pdm-python` file.

### Developing without PDM

In this case, you can still use another package manager supporting [PEP 621](https://peps.python.org/pep-0621/) to install _non development dependecies_, as Python has still not standardized specifying development dependencies, although the pending [PEP 735](https://peps.python.org/pep-0735/) seeks to change this. Therefore, no matter your alternative package manager, you will have to install the development dependencies manually. Additionally, if your package manager of choice does not support PEP 621, you will also have to install the regular dependencies manually.

In the following example, we will use [pip](https://pip.pypa.io/), the de-facto standard for Python package management. We assume a sufficient version of pip, with PEP 621 support, is already installed, and _do not_ detail the creation of a Virtual Environment. For creating a Virtual Environment, see [this](https://packaging.python.org/en/latest/tutorials/installing-packages/#optionally-create-a-virtual-environment). **If you continue without creating a Virtual Environment, pip will install the dependencies globally**.

First, we will install the required dependencies in our environment by running:

```bash
pip install -e <PATH-TO-PDDLSIM-DIRECTORY>
```

where `<PATH-TO-PDDLSIM-DIRECTORY>` should be replaced by the path to the directory containing the PDDLSIM project's source files. Assuming this is the current working directory, one may run:

```bash
pip install -e .
```

Note that the above commands will install PDDLSIM in editable mode. This is generally preferred for development. You can drop the `-e` flag install regularly.

As a reminder, to also be able to build the documentation, run tests, etc., you will need to install the development dependencies manually. Naturally, they are found in `pyproject.toml`, under `[tool.pdm.dev-dependencies]`.

### Building the documentation

Once you have a development environment setup, with the `doc` development dependency group, run:

```bash
sphinx-build <ROOT-PROJECT-DIRECTORY>/docs/ <BUILD-DIRECTORY>
```

where `<ROOT-PROJECT-DIRECTORY>` is the root directory of the PDDLSIM source (i.e., the one containing `pyproject.toml`), and `<BUILD-DIRECTORY>` is a directory to place the documentation artifacts in. When already in the root project directory, usually one might run:

```bash
    sphinx-build docs/ build/
```

When the build artifact directory is within the root project directory, its name should be `build`, as it is explicitly mentioned in the `.gitignore`. When using a different artifact name, make sure to not stage it when comitting.

Once you finish building the documentation, open `<BUILD-DIRECTORY>/index.html` in your preferred web browser to inspect the documentation.


[^1]: This is despite the fact the project is named **PDDL**SIM and not **PPDDL**SIM.
[^2]: Some PDDL features, like those not featured in classical planning, are unsupported, and some extensions are present.
