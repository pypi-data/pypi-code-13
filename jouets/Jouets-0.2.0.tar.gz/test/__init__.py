#!/usr/bin/env python3

# Copyright 2014-2015 Louis Paternault
#
# This file is part of Jouets.
#
# Jouets is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jouets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jouets.  If not, see <http://www.gnu.org/licenses/>.

"""Tests"""

import os
import unittest

import jouets

def suite():
    """Renvoie un objet TestSuite, pour tester l'ensemble de `jouets`.
    """
    test_loader = unittest.defaultTestLoader
    return test_loader.discover(
        os.path.abspath(os.path.join(jouets.__path__[0], ".."))
        )

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
