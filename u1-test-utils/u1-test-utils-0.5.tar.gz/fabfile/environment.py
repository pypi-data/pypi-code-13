# -*- coding: utf-8 -*-

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
import sys

from fabric.api import env, local


VIRTUALENV = '.env'


def bootstrap():
    local('rm -rf %s' % VIRTUALENV)
    local("find -name '*.pyc' -delete")
    setup_virtualenv()
    _install_dependencies()


def setup_virtualenv():
    created = False
    virtual_env = os.environ.get('VIRTUAL_ENV', None)
    if virtual_env is None:
        if not os.path.exists(VIRTUALENV):
            _create_virtualenv()
            created = True
        virtual_env = VIRTUALENV
    env.virtualenv = os.path.abspath(virtual_env)
    _activate_virtualenv()
    return created


def _create_virtualenv():
    if not os.path.exists(VIRTUALENV):
        virtualenv_bin_path = local('which virtualenv', capture=True)
        virtualenv_version = local('{0} {1} --version'.format(
            sys.executable, virtualenv_bin_path), capture=True)
        # We only care about major.minor revision numbers
        version_strings = virtualenv_version.split('.')[0:1]
        virtualenv_version = [int(x) for x in version_strings]
        args = '--distribute --clear'
        if virtualenv_version < [1, 7]:
            args += ' --no-site-packages'
        local('{0} {1} {2} {3}'.format(sys.executable, virtualenv_bin_path,
            args, VIRTUALENV), capture=False)


def _activate_virtualenv():
    activate_this = os.path.abspath(
        '{0}/bin/activate_this.py'.format(env.virtualenv))
    execfile(activate_this, dict(__file__=activate_this))
    # Work around fabric unconditionally removing first entry in sys.path by
    # adding a dummy one. Agreed with Leo on IRC that the workaround is ok as
    # the plan is to stop using fabric in the long run and the bug itself is a
    # blocker. -- vila 2013-09-25
    sys.path.insert(0, '/I-dont-exist-blow-me-away-I-dont-care')


def _install_dependencies():
    # it's possible to get "ImportError: No module named setuptools"
    # when using pip<1.4 to upgrade a package that depends on setuptools.
    run_in_virtualenv_local('pip install -U setuptools', capture=False)
    run_in_virtualenv_local(
        'pip install -U -r requirements.txt', capture=False)


def run_in_virtualenv_local(command, capture=True):
    prefix = ''
    virtual_env = env.get('virtualenv', None)
    if virtual_env:
        prefix = '. {0}/bin/activate && '.format(virtual_env)
    command = prefix + command
    return local(command, capture=capture)
