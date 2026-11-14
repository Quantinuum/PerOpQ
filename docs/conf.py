"""Sphinx configuration."""

project = "PerOpQ"
copyright = "2023, Quantinuum"
author = "Quantinuum"

extensions = [
    "sphinx.ext.autodoc",
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "myst_parser",
]
autoapi_dirs = ["../src"]
autoapi_add_toctree = False
# The legacy file imports the removed peropq.pauli module. The supported
# small-system reference is implemented in ed_module.py.
autoapi_ignore = ["*/exact_diagonalization.py"]
autodoc_typehints = "description"
html_theme = "furo"
