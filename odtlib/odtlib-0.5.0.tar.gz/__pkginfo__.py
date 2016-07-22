"""Ovcs packaging information.

:organization: Logilab
:copyright: 2008-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: General Public License version 2 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"
from glob import glob

# pylint: disable-msg=W0622

# package name
modname = distname = 'odtlib'

# release version
numversion = (0, 5, 0)
version = '.'.join(str(num) for num in numversion)

# license and copyright
license = 'GPL'
copyright = 'Copyright (c) '+' '.join([line.split(': ')[-1]for line in __doc__.splitlines()[3:5]])

# description
description = "utility to check & fix odt files"

# author name and email
author = "Logilab"
author_email = "contact@logilab.fr"

# home page (not existing)
web = "http://www.logilab.org/project/%s" % modname

# mailing list
mailinglist = 'mailto://python-projects@lists.logilab.org'

# download place
# ftp = "ftp://ftp.logilab.org/pub/%s" % modname

# is there some directories to include with the source installation
include_dirs = []

# executable

scripts = []

pyversions = ['2.5']

# data files
data_files = glob('i18n/*/*/*') # ['i18n/fr/LC_MESSAGES/odtlib.mo']

