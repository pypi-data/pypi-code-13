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

from silentdune_client.modules.firewall.manager.slots import Slots
from silentdune_client.builders import iptables as ipt
from silentdune_client.modules.automation.auto_discovery.base_discovery_service import BaseDiscoveryService
from silentdune_client.modules.firewall.manager.iptables_utils import create_iptables_tcp_ingress_egress_rule, create_iptables_udp_ingress_egress_rule

_logger = logging.getLogger('sd-client')


class SecureSHellDiscovery(BaseDiscoveryService):
    """
    Auto discover SSH.
    """

    _slot = Slots.admin  # SSH is administration.
    _config_property_name = '_disable_auto_ssh'

    def _discover_iptables(self):

        rules = list()
        conf = u'/etc/ssh/sshd_config'
        port = 22

        if not os.path.exists(conf):
            _logger.error('{0}: sshd_config not found.'.format(self.get_name()))
            return None

        # Get all nameserver ip address values
        with open(conf) as handle:
            for line in handle:
                if line.strip().startswith(u'Port '):
                    port = int(line.split(u'Port')[1])

        _logger.debug('{0}: adding SSH Server Rules.'.format(self.get_name()))
        rules.append(create_iptables_tcp_ingress_egress_rule(None, port, self._slot, transport=ipt.TRANSPORT_IPV4))
        rules.append(create_iptables_tcp_ingress_egress_rule(None, port, self._slot, transport=ipt.TRANSPORT_IPV6))

        return rules
