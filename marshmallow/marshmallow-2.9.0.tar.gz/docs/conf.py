# -*- coding: utf-8 -*-
#
# marshmallow documentation build configuration file.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os
import datetime as dt

import alabaster
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('..'))
import marshmallow
from marshmallow.compat import OrderedDict

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'alabaster',
    'sphinx_issues',
]

primary_domain = 'py'
default_role = 'py:obj'

intersphinx_mapping = {
    'python': ('http://python.readthedocs.io/en/latest/', None),
}

issues_github_path = 'marshmallow-code/marshmallow'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'
# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'marshmallow'
copyright = ' {0:%Y} <a href="http://stevenloria.com">Steven Loria</a>'.format(
    dt.datetime.utcnow()
)

version = release = marshmallow.__version__

exclude_patterns = ['_build']

# THEME

html_theme_path = [alabaster.get_path()]
html_theme = 'alabaster'
html_static_path = ['_static']
templates_path = ['_templates']
html_show_sourcelink = False

html_theme_options = {
    'logo': 'marshmallow-logo.png',
    'description': 'Object serialization and deserialization, lightweight and fluffy.',
    'description_font_style': 'italic',
    'github_user': 'marshmallow-code',
    'github_repo': 'marshmallow',
    'github_banner': True,
    'github_type': 'star',
    'gratipay_user': 'sloria',
    'code_font_size': '0.8em',
    'warn_bg': '#FFC',
    'warn_border': '#EEE',
    # Used to populate the useful-links.html template
    'extra_nav_links': OrderedDict([
        ('marshmallow @ PyPI', 'http://pypi.python.org/pypi/marshmallow'),
        ('marshmallow @ GitHub', 'http://github.com/marshmallow-code/marshmallow'),
        ('Issue Tracker', 'http://github.com/marshmallow-code/marshmallow/issues'),
    ])
}

html_sidebars = {
    'index': [
        'about.html', 'useful-links.html', 'searchbox.html', 'donate.html',
    ],
    '**': ['about.html', 'useful-links.html',
           'localtoc.html', 'relations.html', 'searchbox.html', 'donate.html']
}
