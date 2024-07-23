Building and publishing PDDLSIM releases
========================================

If you do not have a development environment set up, see :ref:`development-setup`. Once you do have one however, building instructions will vary depending on how you are developing on PDDLSIM.

Building and publishing with PDM
--------------------------------

When using `PDM <https://pdm-project.org>`_, the process is relatively straightforward. *From* the root project directory, meaning the one that contains ``pyproject.toml``, run:

.. code-block:: bash

    pdm publish

If you only wish to build PDDLSIM, run instead:

.. code-block:: bash

    pdm build

and the build artifacts will be available in ``.pdm-build/``.

Building without PDM
--------------------

To build without PDM, see `this <https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives>`_. Note that building will still use `PDM-Backend <https://backend.pdm-project.org/>`_, as seen in the project's ``pyproject.toml``. Then, to publish to PyPI, use a tool such as `Twine <https://twine.readthedocs.io/en/>`_, as seen in `here <https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives>`_.