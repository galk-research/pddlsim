The PDDLSIM simulator
=====================

PDDLSIM is a simulator for a PPDDL-like language [#project_name]_ [#supported_features]_, with a supporting library to define agents and interface with said simulator, locally, or via a remote connection. PDDLSIM was created for the Bar-Ilan University course `"Introduction to Intelligent, Cognitive, and Knowledge-Based Systems" (89-674) <https://u.cs.biu.ac.il/~kaminkg/teach/current/intsys/>`_.

Installation
------------

PDDLSIM is available on `PyPI <https://pypi.org/project/pddlsim/>`_, requiring no external dependencies. Note that PDDLSIM requires on Python 3.12 or later. Earlier, legacy versions of PDDLSIM are also available on PyPI, but are unsupported.

User Guide
----------

How to setup PDDLSIM, some common and useful parts of the API, info on using PDDLSIM for some tasks, and more.

.. toctree::
    :maxdepth: 3

    user_guide/index

Contributor Guide
-----------------

How to contribute changes to PDDLSIM, details on the internals of PDDLSIM, and some specifications and workflows, among other things.

.. toctree::
    :maxdepth: 3

    contributor_guide/index

.. rubric:: Footnotes

.. [#project_name] This is despite the fact the project is named **PDDL**\ SIM and not **PPDDL**\ SIM.
.. [#supported_features] Some PDDL features, like those not featured in classical planning, are unsupported, and some extensions are present.