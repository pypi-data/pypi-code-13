# Copyright 2012, 2013 Canonical Ltd.
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

import os
import unittest

from fabric import api


def test(*test_regexps):
    """Run tests.

    :param test_regexps: A list of test regexps to include.
    """
    # late import to ensure the virtual env is active
    from sst import (
        filters,
        loaders,
        )
    os.environ['DJANGO_SETTINGS_MODULE'] = \
        'u1testutils.selftests.django_project.settings'

    loader = loaders.TestLoader()
    suite = loader.suiteClass()
    suite.addTests(loader.discoverTestsFromTree('u1testutils'))
    suite.addTests(loader.discoverTestsFromTree('setup_vm'))

    suite = filters.include_regexps(test_regexps, suite)

    # List the tests as we run them
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    print 'Totals: ran({0}), skipped({1}), errors({2}), failures({3})'.format(
        res.testsRun, len(res.skipped), len(res.errors), len(res.failures))
    if not res.wasSuccessful():
        api.abort('Tests failed.')
