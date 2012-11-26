# -*- coding: utf-8 -*-
#

import sys, os

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'GerritBot'
copyright = u'2012, OpenStack Continuous Integration Administrators'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'default'

# Output file base name for HTML help builder.
htmlhelp_basename = 'GerritBotdoc'

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'gerritbot', u'GerritBot Documentation',
     [u'OpenStack Continuous Integration Administrators'], 1)
]
