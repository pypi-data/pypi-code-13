#
# Authors: Ma He <mahe.itsec@gmail.com>
#
# Copyright (C) 2015-2016 EntPack
# see file 'LICENSE' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
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
#

import logging
import os
import subprocess
import shlex

from silentdune_client.modules.firewall.manager.slots import Slots
from silentdune_client.builders import iptables as ipt
from silentdune_client.modules.automation.auto_discovery.base_discovery_service import BaseDiscoveryService
from silentdune_client.modules.firewall.manager.iptables_utils import create_iptables_udp_egress_ingress_rule
from silentdune_client.utils.misc import which

_logger = logging.getLogger('sd-client')


class NetworkTimeProtocolDiscovery(BaseDiscoveryService):
    """
    Auto discover NTP.
    """

    _slot = Slots.ntp
    _config_property_name = '_disable_auto_ntp'

    def _discover_iptables(self):

        rules = list()

        ntpq = which(u'ntpq')
        if not ntpq:
            _logger.debug('Failed to find program path for "{0}"'.format(u'ntpq'))
            return rules;

        p = subprocess.Popen([u'ntpq', u'-p', u'-n'], stdout=subprocess.PIPE)
        stdoutdata, stderrdata  = p.communicate()
        result = p.wait()
        
        if stderrdata == None :
            for line in stdoutdata.split(b'\n'):
                item = line.split(b' ', 1)
                if item[0][:1] == b'+' or item[0][:1] == b'-' or item[0][:1] == b'*' or item[0][:1] == b'x' or item[0][:1] == b'.' or item[0][:1] == b'#' or item[0][:1] == b'o':
                    ipaddr = item[0][1:]

                    _logger.debug('{0}: adding NTP Client Rules for {1}'.format(self.get_name(), ipaddr))
                    rules.append(create_iptables_udp_egress_ingress_rule(ipaddr.decode("utf-8"), 123, self._slot, transport=ipt.TRANSPORT_AUTO))

        return rules
