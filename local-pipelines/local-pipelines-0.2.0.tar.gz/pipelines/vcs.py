# vi:et:ts=4 sw=4 sts=4
#
# local-pipelines : run Bitbucket pipelines locally
# Copyright (C) 2016  Gary Kramlich <grim@reaperworld.com>
# Copyright (C) 2016  Sean Farley <sean@farley.io>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

import os
import subprocess


_VCSS = {
    'git': 'git rev-parse --abbrev-ref HEAD -C {}',
    'hg': 'hg branch -R {}',
}


def get_branch(path):
    branch = None
    env = os.environ.copy()

    # ignore user's config
    env['HGRCPATH'] = '/dev/null'
    env['HOME'] = '/tmp'
    env['GIT_CONFIG_NOSYSTEM'] = '1'

    for _, cmd in _VCSS.iteritems():
        try:
            command = cmd.format(path)
            branch = subprocess.check_output(command.split(),
                                             stderr=open(os.devnull, 'w'),
                                             env=env)
            branch = branch.strip()
        except subprocess.CalledProcessError:
            pass

    return branch
