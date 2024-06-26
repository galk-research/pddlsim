# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/uensage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "PDDLSIM"
project_copyright = "2024, Gal A. Kaminka and others"
author = "Gal A. Kaminka and others"
release = "0.2.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_design"]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "navbar_center": ["version-switcher", "navbar-nav"],
    "icon_links": [
        {
            "name": "BitBucket",
            "url": "https://bitbucket.org/galk-opensource/executionsimulation/",
            "icon": "fa-brands fa-bitbucket",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/pddlsim",
            "icon": "fa-brands fa-python",
        },
    ],
    "footer_start": ["copyright"],
    "footer_center": ["sphinx-version"],
    "logo": {
        "image_light": "pddlsim-light.svg",
        "image_dark": "pddlsim-dark.svg",
    },
}
html_static_path = ["_static"]
