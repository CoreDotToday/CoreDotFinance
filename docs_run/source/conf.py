# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path

lib_file = os.path.abspath("../..")
sys.path.insert(0, lib_file)


# -- Project information -----------------------------------------------------

project = "CoreDotFinance"
copyright = "2021, Core.Today"
author = "Core.Today"

html_title = project
html_show_sourcelink = False


# The full version, including alpha/beta/rc tags

import re

target = os.path.join(lib_file, "coredotfinance", "__init__.py")


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ""
    with open(fname, "r") as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError("Cannot find version information")
    return version


__version__ = find_version(target)
release = __version__

print(release)

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_panels",
    "sphinx.ext.extlinks",
    "sphinx.ext.autosummary",
    "nbsphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "kr"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = "sphinx_material"
html_favicon = "favicon.ico"
html_css_files = []
# Material theme options (see theme.conf for more information)
html_theme_options = {
    # Set the name of the project to appear in the navigation.
    "nav_title": "CoreDotFinance",
    # Set you GA account ID to enable tracking
    # 'google_analytics_account': 'UA-XXXXX',
    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    "base_url": "https://coredottoday.github.io/CoreDotFinance",
    # Set the color and the accent color
    "color_primary": "amber",
    "color_accent": "green",
    # Set the repo location to get a badge with stats
    "repo_url": "https://github.com/CoreDotToday/CoreDotFinance",
    "repo_name": "CoreDotFinance",
    "repo_type": "github",
    # Visible levels of the global TOC; -1 means unlimited
    "globaltoc_depth": 1,
    # If False, expand all TOC entries
    "globaltoc_collapse": True,
    # If True, show hidden TOC entries
    "globaltoc_includehidden": False,
    "html_minify": False,
    "css_minify": False,
    "master_doc": False,
}

# pygments_style = "default"

html_sidebars = {"**": ["globaltoc.html", "localtoc.html", "searchbox.html"]}

# ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_logo = "./_static/coredottoday1.png"

# -- nbsphinx configuration ----------------------------------------------
