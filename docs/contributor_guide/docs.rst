Documentation
=============

The documentation for the project is built using `Sphinx <https://www.sphinx-doc.org/>`__, and the `PyData Sphinx Theme <https://pydata-sphinx-theme.readthedocs.io/>`__. For more information on the documentation development dependencies, consult PDDLSIM's ``pyproject.toml``.

XXX Yoav, it's fine to point to the tools, but note that you are sending the reader to look for instructions on how to install.  This is waaaay to much work, just to read a manual!


Building the documentation
--------------------------

If you do not have a development environment set up, see :ref:`Development setup`. Once you have a development environment setup, with the ``doc`` development dependency group, run:

.. code-block:: bash

    sphinx-build <ROOT-PROJECT-DIRECTORY>/docs/ <BUILD-DIRECTORY>

where ``<ROOT-PROJECT-DIRECTORY>`` is the root directory of the PDDLSIM source (i.e., the one containing ``pyproject.toml``), and ``<BUILD-DIRECTORY>`` is a directory to place the documentation artifacts in. When already in the root project directory, usually one might run:

.. code-block:: bash

    sphinx-build docs/ build/

XXXX Yoav: It does not work. I've tried installing sphinx both via pip, and via apt install (per the instructions on their own web site). Both methods result in a version that
does not work with the docs folder as it is here. This is a clear symptom of a the worst type of packaging a product:   It was tested only on
the developer's machine, and not on a clean machine.


When the build artifact directory is within the root project directory, its name should be ``build``, as it is explicitly mentioned in the ``.gitignore``. When using a different artifact name, make sure to not stage it when comitting.

Once you finish building the documentation, open ``<BUILD-DIRECTORY>/index.html`` in your preferred web browser to inspect the documentation.

Extending the documentation
---------------------------

Beyond following the usual steps for contributing code to the project, the process is fairly similar to that of another project using Sphinx. The documentation is written in `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`__. Because we use the PyData Sphinx Theme, some documentation files may use extra elements, as described in `here <https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/theme-elements.html>`__. Naturally, you may use these extra elements in your contribution.
