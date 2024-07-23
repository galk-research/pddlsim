.. _development-setup:

Development setup
=================

PDDLSIM uses `PDM <https://pdm-project.org>`__ as its build tool and dependency manager. To work on PDDLSIM, it is recommended, but not strictly required you use it, while developing PDDLSIM. PDM is PDDLSIM's build backend, and is additionally used to specify development dependencies (via ``tool.pdm.dev-dependencies``), that need to be installed for performing various development related tasks, e.g. running tests utilizing ``pytest`` (and some extra plugins), building the documentation using Sphinx (and the required theme and extensions), etc.

### Developing with PDM

To use PDM with the project, first install PDM. See `this <https://pdm-project.org/latest/#installation>`__ for more information on installation. Once you have PDM installed run:

.. code-block:: bash
    
    pdm use

And select a base interpreter, to configure a Virtual Environment for development. Then, get the command for activating the Virtual Environment with:

.. code-block:: bash
    
    pdm venv activate

And run the command. You will now be inside the Virtual Environment, which is currently *empty*. To install *all* of PDDLSIM's dependencies, *including development-related* ones, such that PDDLSIM is in editable mode, run:

.. code-block:: bash

    pdm install

To *avoid* installing development dependencies, add the ``--production`` flag. Additionally, you can prevent any local package being installed in editable mode by using the ``--no-editable`` flag. Other options are by using the ``--help`` flag. 

At this stage, you should be able to begin development with no issue. Make sure to the newly created Python interpreter to your code editor. Its path can be found in the ``.pdm-python`` file.

### Developing without PDM

In this case, you can still use another package manager supporting `PEP 621 <https://peps.python.org/pep-0621/>`__ to install *non development dependecies*, as Python has still not standardized specifying development dependencies, although the pending `PEP 735 <https://peps.python.org/pep-0735/>`__ seeks to change this. Therefore, no matter your alternative package manager, you will have to install the development dependencies manually. Additionally, if your package manager of choice does not support PEP 621, you will also have to install the regular dependencies manually.

In the following example, we will use `pip <https://pip.pypa.io/>`__, the de-facto standard for Python package management. We assume a sufficient version of pip, with PEP 621 support, is already installed, and *do not* detail the creation of a Virtual Environment. For creating a Virtual Environment, see `this <https://packaging.python.org/en/latest/tutorials/installing-packages/#optionally-create-a-virtual-environment>`__.

.. danger::

    If you continue without creating a Virtual Environment, pip will install the dependencies globally.

First, we will install the required dependencies in our environment by running:

.. code-block:: bash

    pip install -e <PATH-TO-PDDLSIM-DIRECTORY>

where ``<PATH-TO-PDDLSIM-DIRECTORY>`` should be replaced by the path to the directory containing the PDDLSIM project's source files. Assuming this is the current working directory, one may run:

.. code-block:: bash

    pip install -e .

Note that the above commands will install PDDLSIM in editable mode. This is generally preferred for development. You can drop the ``-e`` flag install regularly.

As a reminder, to also be able to build the documentation, run tests, etc., you will need to install the development dependencies manually. Naturally, they are found in ``pyproject.toml``, under ``[tool.pdm.dev-dependencies]``.