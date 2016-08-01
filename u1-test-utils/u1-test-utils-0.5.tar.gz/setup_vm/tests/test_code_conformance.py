# Copyright 2013 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License version 3, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import setup_vm

from u1testutils.static import (
    test_pep8_conformance as pep8,
    test_pyflakes_analysis as pyflakes,
)


class Pep8ConformanceTestCase(pep8.Pep8ConformanceTestCase):

    packages = [setup_vm]


class PyflakesAnalysisTestCase(pyflakes.PyflakesAnalysisTestCase):

    packages = [setup_vm]
