# pylint: disable=W0622,C0103
# Copyright (c) 2003-2014 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""pylint packaging information"""
from __future__ import absolute_import

import sys
from os.path import join

modname = distname = 'pwclip'

numversion = (0, 0, 1)
version = '.'.join([str(num) for num in numversion])

install_requires = [
    'pyusb',
    'yubico',
]

license = 'GPL'
description = "secure password clip (copy/paste) via python3-yubico"
web = 'http://janeiskla.de'
mailinglist = ""
author = 'Leon Pelzer'
author_email = 'mail@leonpelzer.de'

classifiers = ['Development Status :: 4 - Beta',
               'Environment :: Console',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: GNU General Public License (GPL)',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development :: Debuggers',
               'Topic :: Software Development :: Quality Assurance',
               'Topic :: Software Development :: Testing'
              ]


long_desc = """\
  provides a multi-platform leight-weight gui implementing a secure & convienient (yubikey) user-challenge-response"""

scripts = [join('bin', 'pwclip')]
include_dirs = [join('pwclip')]
