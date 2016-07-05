# -*- coding: utf-8  -*-
"""Package for tests."""

# Copyright (C) 2015 Alexander Jones
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import sys
import unittest


PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3


class TestCase(unittest.TestCase):

    """Subclass of unittest.TestCase."""

    if PY2:

        def assertCountEqual(self, *args, **kwargs):
            """Wrapper of assertItemsEqual()."""
            return self.assertItemsEqual(*args, **kwargs)
