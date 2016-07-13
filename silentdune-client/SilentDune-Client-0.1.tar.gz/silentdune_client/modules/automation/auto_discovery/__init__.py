#
# Authors: Robert Abram <robert.abram@entpack.com>
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

import ast
import hashlib
import logging
import socket
import sys

from silentdune_client.utils.module_loading import import_by_str
from silentdune_client.modules import BaseModule, QueueTask
from silentdune_client.modules.firewall.manager.slots import Slots
from silentdune_client.modules.firewall.manager import SilentDuneClientFirewallModule, \
    TASK_FIREWALL_INSERT_RULES, TASK_FIREWALL_DELETE_RULES, TASK_FIREWALL_ALLOW_ALL_DNS_ACCESS, \
    TASK_FIREWALL_DISABLE_ALL_DNS_ACCESS, TASK_FIREWALL_DISABLE_ALL_NTP_ACCESS, TASK_FIREWALL_ALLOW_ALL_NTP_ACCESS

_logger = logging.getLogger('sd-client')

module_list = {
    'Silent Dune Auto Service Discovery': {
        'module': 'SilentDuneAutoServiceDiscoveryModule',
    },
}

AUTO_DISCOVERY_SERVICE_LIST = (
    "silentdune_client.modules.automation.auto_discovery.lo.LoopbackDiscovery",  # Slot 100
    "silentdune_client.modules.automation.auto_discovery.ssh.SecureSHellDiscovery",  # Slot 110
    "silentdune_client.modules.automation.auto_discovery.dns.DynamicNameServiceDiscovery",  # Slot 130
    "silentdune_client.modules.automation.auto_discovery.ntp.NetworkTimeProtocolDiscovery",  # Slot 140
    "silentdune_client.modules.automation.auto_discovery.updates.SystemUpdatesDiscovery",  # Slot 150
    "silentdune_client.modules.automation.auto_discovery.dhcp.DynamicHostConfigurationProtocolDiscovery",  # Slot 170
    "silentdune_client.modules.automation.auto_discovery.icmp.IcmpDiscovery",  # Slot 180
    "silentdune_client.modules.automation.auto_discovery.reject.RejectRuleDiscovery",  # Slot 9900
    # Identity services (LDAP, FreeIPA, ...)  # Slot 160
)

NTP_DISCOVERY_SERVICE = "silentdune_client.modules.automation.auto_discovery.ntp.NetworkTimeProtocolDiscovery"


class SilentDuneAutoServiceDiscoveryModule(BaseModule):
    """
    Auto discover required external services by this system. IE: DNS, NTP, Updates, DHCP, ...
    """
    # Module properties
    _disable_auto_lo = False
    _disable_auto_ssh = False
    _disable_auto_dns = False
    _disable_auto_ntp = False
    _disable_auto_updates = False
    _disable_auto_updates_ftp = False
    _disable_auto_updates_rsync = False
    _disable_auto_dhcp = False
    _disable_auto_icmp = False
    _disable_auto_reject = False

    # Timed events
    _t_all_service_check = 0  # Counter for next all service check
    _t_all_check_interval = 3600  # One hour

    _t_ntp_service_check = 0  # Counter for next NTP service check
    _t_ntp_check_interval = 300  # Five minutes

    _startup = True
    _all_dns_access_enabled = False
    _all_ntp_access_enabled = False

    _mss_slots = {}  # Storage for machine_subset hashes and slot ids.  For detection of rule changes.

    def __init__(self):

        self._arg_name = 'autodiscover'  # Set argparser name
        self._config_section_name = 'auto_discovery'  # Set configuration file section name

        # Enable multi-threading
        self.wants_processing_thread = True

        self._enabled = False

    def add_installer_arguments(self, parser):
        """
        Virtual Override
        Add our module's argparser arguments
        """

        # Create a argument group for our module
        group = parser.add_argument_group('auto discovery module', 'Silent Dune Auto Discovery module')

        group.add_argument('--discovery-mod-enable', action='store_false',  # noqa
                           help=_('Enable the auto discovery module'))  # noqa

        group.add_argument(_('--disable-auto-lo'), help=_('Disable auto Loopback rules.'),  # noqa
                           default=False, action='store_true')  # noqa
        group.add_argument(_('--disable-auto-ssh'), help=_('Disable auto SSH rules.'),  # noqa
                           default=False, action='store_true')  # noqa
        group.add_argument(_('--disable-auto-dns'), help=_('Disable auto DNS discovery.'),  # noqa
                           default=False, action='store_true')  # noqa
        group.add_argument(_('--disable-auto-ntp'), help=_('Disable auto NTP discovery.'),  # noqa
                           default=False, action='store_true')  # noqa
        group.add_argument(_('--disable-auto-updates'), help=_('Disable auto System Updates discovery.'),  # noqa
                           default=False, action='store_true')  # noqa
        group.add_argument(_('--disable-auto-dhcp'), help=_('Disable auto DHCP discovery.'),  # noqa
                           default=False, action='store_true')  # noqa
        group.add_argument(_('--disable-auto-icmp'), help=_('Disable auto ICMP discovery.'),  # noqa
                           default=False, action='store_true')  # noqa
        group.add_argument(_('--disable-auto-reject'), help=_('Disable auto rejection rules.'),  # noqa
                           default=False, action='store_true')  # noqa

    def validate_arguments(self, args):
        """
        Virtual Override
        Validate command line arguments and save values to our configuration object.
        :param args: An argparse object.
        """

        # Check for conflicting arguments.
        if (not '--discovery-mod-enable' in sys.argv) and (
                '--disable-auto-lo' in sys.argv or
                '--disable-auto-dns' in sys.argv or
                '--disable-auto-reject' in sys.argv or
                '--disable-auto-ntp' in sys.argv or
                '--disable-auto-updates' in sys.argv or
                '--disable-auto-dhcp' in sys.argv or
                '--disable-auto-icmp' in sys.argv or
                '--disable-auto-ssh' in sys.argv):
            print('sdc-install: argument --discovery-mod-enable conflicts with other auto discover module arguments.')
            return False

        if args.discovery_mod_enable:
            self._enabled = True
            return True

        # Check for any required arguments here

        self._disable_auto_lo = args.disable_auto_lo
        self._disable_auto_ssh = args.disable_auto_ssh
        self._disable_auto_dns = args.disable_auto_dns
        self._disable_auto_ntp = args.disable_auto_ntp
        self._disable_auto_updates = args.disable_auto_updates
        self._disable_auto_updates_ftp = args.disable_auto_updates_ftp
        self._disable_auto_updates_rsync = args.disable_auto_updates_rsync
        self._disable_auto_dhcp = args.disable_auto_dhcp
        self._disable_auto_icmp = args.disable_auto_icmp
        self._disable_auto_reject = args.disable_auto_reject

        return True

    def validate_config(self, config):
        """
        Virtual Override
        Validate configuration file arguments and save values to our config object.
        :param config: A ConfigParser object.
        """

        # See if we are enabled or not
        try:
            self._enabled = True if config.get(self._config_section_name, 'enabled').lower() == 'yes' else False
        except:
            _logger.debug('{0} configuration section not found in configuration file.'.format(
                self._config_section_name))
            self._enabled = False

        # Only worry about the rest of the configuration items if we are enabled.
        if self._enabled:

            self._disable_auto_lo = True if config.get(self._config_section_name, 'disable_auto_lo').lower() == 'yes' else False
            self._disable_auto_ssh = True if config.get(self._config_section_name, 'disable_auto_ssh').lower() == 'yes' else False
            self._disable_auto_dns = True if config.get(self._config_section_name, 'disable_auto_dns').lower() == 'yes' else False
            self._disable_auto_ntp = True if config.get(self._config_section_name, 'disable_auto_ntp').lower() == 'yes' else False
            self._disable_auto_updates = True if config.get(self._config_section_name, 'disable_auto_updates').lower() == 'yes' else False
            self._disable_auto_updates_ftp = True if config.get(self._config_section_name, 'disable_auto_updates_ftp').lower() == 'yes' else False
            self._disable_auto_updates_rsync = True if config.get(self._config_section_name, 'disable_auto_updates_rsync').lower() == 'yes' else False
            self._disable_auto_dhcp = True if config.get(self._config_section_name, 'disable_auto_dhcp').lower() == 'yes' else False
            self._disable_auto_icmp = True if config.get(self._config_section_name, 'disable_auto_icmp').lower() == 'yes' else False
            self._disable_auto_reject = True if config.get(self._config_section_name, 'disable_auto_reject').lower() == 'yes' else False

        return True

    def prepare_config(self, config):
        """
        Virtual Override
        Return the configuration file structure. Any new configuration items should be added here.
        Note: The order should be reverse of the expected order in the configuration file.
        """

        config.set(self._config_section_name, 'enabled', 'yes' if self._enabled else 'no')
        config.set(self._config_section_name, 'disable_auto_lo', 'yes' if self._disable_auto_lo else 'no')
        config.set(self._config_section_name, 'disable_auto_ssh', 'yes' if self._disable_auto_ssh else 'no')
        config.set(self._config_section_name, 'disable_auto_dns', 'yes' if self._disable_auto_dns else 'no')
        config.set(self._config_section_name, 'disable_auto_ntp', 'yes' if self._disable_auto_ntp else 'no')
        config.set(self._config_section_name, 'disable_auto_updates', 'yes' if self._disable_auto_updates else 'no')
        config.set(self._config_section_name, 'disable_auto_updates_ftp', 'yes' if self._disable_auto_updates_ftp else 'no')
        config.set(self._config_section_name, 'disable_auto_updates_rsync', 'yes' if self._disable_auto_updates_rsync else 'no')
        config.set(self._config_section_name, 'disable_auto_dhcp', 'yes' if self._disable_auto_dhcp else 'no')
        config.set(self._config_section_name, 'disable_auto_icmp', 'yes' if self._disable_auto_icmp else 'no')
        config.set(self._config_section_name, 'disable_auto_reject', 'yes' if self._disable_auto_reject else 'no')

        config.set_comment(self._config_section_name, self._config_section_name,
                           _('; Silent Dune Auto Discovery Module Configuration\n'))  # noqa
        config.set_comment(self._config_section_name, 'disable_auto_lo',
                           _('; Disable the auto Loopback rule generation.\n'))  # noqa
        config.set_comment(self._config_section_name, 'disable_auto_ssh',
                           _('; Disable the auto SSH ingress rule generation.\n'))  # noqa
        config.set_comment(self._config_section_name, 'disable_auto_dns',
                           _('; Disable the auto DNS egress rule generation.\n'))  # noqa
        config.set_comment(self._config_section_name, 'disable_auto_ntp',
                           _('; Disable the auto NTP egress rule generation.\n'))  # noqa
        config.set_comment(self._config_section_name, 'disable_auto_updates',
                           _('; Disable the auto System Update egress rule generation.\n'))  # noqa
        config.set_comment(self._config_section_name, 'disable_auto_updates_ftp',
                           _('; Disable the auto System Update FTP egress rule generation.\n'))  # noqa
        config.set_comment(self._config_section_name, 'disable_auto_updates_rsync',
                           _('; Disable the auto System Update rsync egress rule generation.\n'))  # noqa
        config.set_comment(self._config_section_name, 'disable_auto_dhcp',
                           _('; Disable the auto DHCP egress rule generation.\n'))  # noqa
        config.set_comment(self._config_section_name, 'disable_auto_icmp',
                           _('; Disable the auto ICMP egress rule generation.\n'))  # noqa
        config.set_comment(self._config_section_name, 'disable_auto_reject',
                           _('; Disable the auto generation of rejection records.\n'))  # noqa

        return True

    def service_startup(self):
        _logger.debug('{0}: module startup called'.format(self.get_name()))

        if not self.validate_config(self.config):
            _logger.error('{0}: module configuration validation failed.'.format(self.get_name()))
            return False

        if not self._enabled:
            return True

        return True

    def service_shutdown(self):
        _logger.debug('{0}: module shutdown called'.format(self.get_name()))

    def process_loop(self):

        if self._startup:

            # Try resolving example.org, if we get an error try enabling generic all DNS access.
            try:
                socket.getaddrinfo('example.org', 80)
            except socket.gaierror:

                # If we have reached here, we have no DNS access at all.
                if self._all_dns_access_enabled:
                    raise OSError('No external DNS access available. Unable to complete auto discovery.')

                _logger.debug('{0}: Asking Firewall Module to enable generic DNS access.'.format(self.get_name()))

                # Tell the firewall manager to enable generic all DNS access.
                self._all_dns_access_enabled = True

                task = QueueTask(TASK_FIREWALL_ALLOW_ALL_DNS_ACCESS,
                                 src_module=self.get_name(),
                                 dest_module=SilentDuneClientFirewallModule().get_name())
                self.send_parent_task(task)

                return

            self._startup = False
            self.discover_services()

            # Tell the firewall manager to remove generic all DNS access rules.
            if self._all_dns_access_enabled:
                self._all_dns_access_enabled = False
                _logger.debug('{0}: Asking Firewall Module to disable generic DNS access.'.format(self.get_name()))
                task = QueueTask(TASK_FIREWALL_DISABLE_ALL_DNS_ACCESS,
                                 src_module=self.get_name(),
                                 dest_module=SilentDuneClientFirewallModule().get_name())
                self.send_parent_task(task)

        # After the check interval has passed, check services again.
        if self.timed_event('_t_all_service_check', self._t_all_check_interval):
            self.discover_services()

        if self._all_ntp_access_enabled and self.timed_event('_t_ntp_service_check', self._t_ntp_check_interval):

            rule_count = self.check_service(NTP_DISCOVERY_SERVICE)

            # If we found NTP rules, tell the firewall manager to remove generic all NTP access rules.
            if self._all_ntp_access_enabled and rule_count > 0:

                self._all_ntp_access_enabled = False
                _logger.debug('{0}: Asking Firewall Module to disable generic NTP access.'.format(self.get_name()))
                task = QueueTask(TASK_FIREWALL_DISABLE_ALL_NTP_ACCESS,
                                 src_module=self.get_name(),
                                 dest_module=SilentDuneClientFirewallModule().get_name())
                self.send_parent_task(task)

    def discover_services(self):
        """
        Loop through the auto discovery class list and call discover() for each class found.
        If any firewall rules are found, send them to the firewall manager service.

        Note: Each slot id used in each discovery class needs to be unique.
        """
        for name in AUTO_DISCOVERY_SERVICE_LIST:
            rule_count = self.check_service(name)

    def check_service(self, name):
        """
        Check the service for rules and add them to the firewall.
        :param name: Service discovery module name
        """
        module_name, class_name = name.rsplit('.', 1)

        _logger.debug('{0}: Loading auto discover object {1}'.format(self.get_name(), class_name))

        module = import_by_str(name)
        cls = module(config=self.config)
        disabled = getattr(self, cls.get_config_property_name())
        if type(disabled) is str:  # Python 2.7 returns string type from getattr(), Python 3.4 returns bool.
            disabled = ast.literal_eval(disabled)

        # _logger.debug('Property: {0}: Value: {1}'.format(cls.get_config_property_name(), disabled))
        # See if this discovery service has been disabled. Name value must match one of our property names.
        if disabled:
            _logger.debug('{0}: {1} discovery service disabled by config.'.format(self.get_name(), class_name))
            return 0

        rules, slot = cls.discover()

        if rules:

            # See if we already have saved rules for this slot id
            if slot in self._mss_slots:
                if self.rules_have_changed(self._mss_slots[slot], rules):

                    _logger.debug('{0}: {1}: Rules have changed, notifying firewall manager.'.format(
                        self.get_name(), class_name))

                    # Notify the firewall module to delete the old rules.
                    task = QueueTask(TASK_FIREWALL_DELETE_RULES,
                                     src_module=self.get_name(),
                                     dest_module=SilentDuneClientFirewallModule().get_name(),
                                     data=self._mss_slots[slot])
                    self.send_parent_task(task)
                else:
                    return 0

            # Save rules so we can check against them next time.
            self._mss_slots[slot] = rules

            # Notify the firewall module to reload the rules.
            task = QueueTask(TASK_FIREWALL_INSERT_RULES,
                             src_module=self.get_name(),
                             dest_module=SilentDuneClientFirewallModule().get_name(),
                             data=rules)
            self.send_parent_task(task)
        else:
            _logger.info('{0}: {1}: discovery service did not return any rules.'.format(
                self.get_name(), class_name))

            _logger.debug('SLOTS: {0}: {1}'.format(Slots.ntp, slot))

            # If there were no rules discovered for NTP, open up access to all NTP servers.
            # In self._t_ntp_check_interval seconds we will check to see if any NTP servers are active.
            if slot == Slots.ntp:
                self._all_ntp_access_enabled = True
                _logger.debug('{0}: Asking Firewall Module to enable generic NTP access.'.format(self.get_name()))
                task = QueueTask(TASK_FIREWALL_ALLOW_ALL_NTP_ACCESS,
                                 src_module=self.get_name(),
                                 dest_module=SilentDuneClientFirewallModule().get_name())
                self.send_parent_task(task)

            return 0

        return len(rules)

    def rules_have_changed(self, old, new):
        """
        Compare rules and see if they are different.
        :param old: List of machine_subset objects
        :param new: List of machine_subset objects
        :return: True if old and new rules are different
        """

        old_rules = ''
        new_rules = ''

        for mss in old:
            old_rules += mss.to_json()

        for mss in new:
            new_rules += mss.to_json()

        return hashlib.sha1(old_rules).hexdigest() != hashlib.sha1(new_rules).hexdigest()
