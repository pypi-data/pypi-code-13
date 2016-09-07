# -*- coding: utf-8 -*-
# Copyright 2016 Antoni Segura Puimedon <celebdor@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import logging
import subprocess

import requests


LOG = logging.getLogger()


def get_scaleway_token(pass_path):
    LOG.info('Getting scaleway token...')
    s = subprocess.Popen(['pass',
                          'show',
                          pass_path],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    outs, errs = s.communicate()

    if not errs:
        token = outs.rstrip()
    else:
        raise ValueError('Failed to retrieve scaleway token. Err: %s' % errs)

    return token


def get_ip(machine, scaleway_token):
    """Returns the IP for a given named machine."""
    LOG.info('Getting machine: %s ip address...', machine)
    req = requests.get(
        'https://api.cloud.online.net/servers',
        headers={'X-Auth-Token': scaleway_token})

    for server in req.json().get('servers', []):
        if server.get('name') == machine:
            public_ip = server.get('public_ip')
            if public_ip is None:
                raise ValueError('No public IP for machine: %s' % machine)
            else:
                return public_ip['address']
    raise ValueError('No machine: %s' % machine)
