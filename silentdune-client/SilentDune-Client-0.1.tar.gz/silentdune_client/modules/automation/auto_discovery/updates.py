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
import platform
import socket
import glob
import ConfigParser
import pycurl

from StringIO import StringIO 

from silentdune_client.modules.firewall.manager.slots import Slots
from silentdune_client.builders import iptables as ipt
from silentdune_client.modules.automation.auto_discovery.base_discovery_service import BaseDiscoveryService
from silentdune_client.modules.firewall.manager.iptables_utils import create_iptables_egress_ingress_rule, create_iptables_egress_rule_dest, create_iptables_ingress_rule_source

_logger = logging.getLogger('sd-client')


class SystemUpdatesDiscovery(BaseDiscoveryService):
    """
    Auto discover SystemUpdates like apt-get and yum.
    """

    _slot = Slots.updates
    _config_section_name = u'auto_discovery'
    _config_property_name = u'_disable_auto_updates'
    _dist = u''
    _dist_version = u''
    _machine = u''
    _disable_auto_updates_ftp = None
    _disable_auto_updates_rsync = None

    _hostnames_http = list()
    _ipaddrs_http = list()

    _hostnames_https = list()
    _ipaddrs_https = list()

    _hostnames_ftp = list()
    _ipaddrs_ftp = list()

    _hostnames_rsync = list()
    _ipaddrs_rsync = list()

    _hostnames_special = list()

    def __init__(self, config):
        super(SystemUpdatesDiscovery, self).__init__(config)
        self._disable_auto_updates_ftp = True if self.config.get(self._config_section_name, u'disable_auto_updates_ftp').lower() == 'yes' else False
        self._disable_auto_updates_rsync = True if self.config.get(self._config_section_name, u'disable_auto_updates_rsync').lower() == 'yes' else False


    def _discover_iptables(self):

        rules = list()

        self._dist = platform.dist()[0]
        self._dist_version=platform.dist()[1]
        self._dist_version = self._dist_version.split(u'.')[0]
        self._machine=platform.machine()

        rules.append(self._iptables_updates())

        return rules


    def _iptables_updates(self):

        rules = list()

        if self._dist == u'Ubuntu':
            rules.append(self._iptables_updates_apt())
        elif self._dist == u'centos':
            rules.append(self._iptables_updates_yum_centos())
        elif self._dist == u'fedora':
            rules.append(self._iptables_updates_yum_fedora())
        else:
            _logger.error('{0}: Distribution is not Ubuntu or CentoS'.format(self.get_name()))

        return rules


    def _iptables_updates_apt(self):

        rules = list()
        hostnames_http = list()
        hostnames_https = list()
        hostnames_ftp = list()
        ipaddrs_http = list()
        ipaddrs_https = list()
        ipaddrs_ftp = list()

        if not os.path.exists(u'/etc/apt/sources.list'):
            _logger.error('{0}: /etc/apt/sources.list not found.'.format(self.get_name()))
            return None

        # Get all nameserver ip address values
        with open(u'/etc/apt/sources.list') as handle:
            for line in handle:
                if u'deb ' in line.lower() and u'http://' in line.lower() and not line.strip().startswith(u'#'):
                    hostname = line.split()[1].split(u'http://')[1].split(u'/')[0]
                    rules.append(self._iptables_updates_http_by_hostname(hostname))
                elif u'deb ' in line.lower() and u'https://' in line.lower() and not line.strip().startswith(u'#'):
                    hostname = line.split()[1].split(u'https://')[1].split(u'/')[0]
                    rules.append(self._iptables_updates_https_by_hostname(hostname))
                elif u'deb ' in line.lower() and u'ftp://' in line.lower() and not line.strip().startswith(u'#'):
                    if self._disable_auto_updates_ftp == False:
                        hostname = line.split()[1].split(u'ftp://')[1].split(u'/')[0]
                        rules.append(self._iptables_updates_ftp_by_hostname(hostname))

        return rules


    def _iptables_updates_yum_centos(self):

        rules = list()
        hostnames_http = list()
        ipaddrs_http = list()

        _logger.debug('{0}: Adding iptables rules for updates of yum for CentOS'.format(self.get_name()))

        Config = ConfigParser.ConfigParser()
        if Config.read(u'/etc/yum.conf') :
            if Config.has_option(u'main', u'bugtracker_url') :
                bugtracker_url = Config.get(u'main', u'bugtracker_url')
                if u'http://' in bugtracker_url.lower() :
                    hostname = bugtracker_url.split(u'http://')[1].split(u'/')[0]
                    rules.append(self._iptables_updates_http_by_hostname(hostname))

        repofiles = glob.glob(u'/etc/yum.repos.d/*.repo')
        for repofile in repofiles :
            Config = ConfigParser.ConfigParser()
            if Config.read(repofile) :
                sections = Config.sections()
                for section in sections :
                    if Config.has_option(section, u'enabled') :
                        enabled = Config.getint(section, u'enabled')
                    else :
                        enabled = 1

                    if enabled == 1 :
                        if Config.has_option(section, u'mirrorlist') :
                            mirrorlist = Config.get(section, u'mirrorlist')
                            if u'http://' in mirrorlist.lower() :
                                hostname = mirrorlist.split(u'http://')[1].split(u'/')[0]
                                rules.append(self._iptables_updates_http_by_hostname(hostname))
                            if u'https://' in mirrorlist.lower() :
                                hostname = mirrorlist.split(u'https://')[1].split(u'/')[0]
                                rules.append(self._iptables_updates_http_by_hostname(hostname))

                            urls = list()
                            urls = self._mirrorlist_to_urls_resolve(mirrorlist)
                            for url in urls :
                                if url.strip().startswith(u'http://') :
                                    hostname = url.split(u'http://')[1].split(u'/')[0]
                                    rules.append(self._iptables_updates_http_by_hostname(hostname))
                                elif url.strip().startswith(u'https://') :
                                    hostname = url.split(u'https://')[1].split(u'/')[0]
                                    rules.append(self._iptables_updates_https_by_hostname(hostname))
                                elif url.strip().startswith(u'ftp://') :
                                    if self._disable_auto_updates_ftp == False :
                                        hostname = url.split(u'ftp://')[1].split(u'/')[0]
                                        rules.append(self._iptables_updates_ftp_by_hostname(hostname))

                        elif Config.has_option(section, u'baseurl') :
                            baseurl = Config.get(section, u'baseurl')
                            if baseurl.strip().startswith(u'http://') :
                                hostname = baseurl.split(u'http://')[1].split(u'/')[0]
                                rules.append(self._iptables_updates_http_by_hostname(hostname))
                            elif baseurl.strip().startswith(u'https://') :
                                hostname = baseurl.split(u'https://')[1].split(u'/')[0]
                                rules.append(self._iptables_updates_https_by_hostname(hostname))
                            elif baseurl.strip().startswith(u'ftp://') :
                                if self._disable_auto_updates_ftp == False :
                                    hostname = baseurl.split(u'ftp://')[1].split(u'/')[0]
                                    rules.append(self._iptables_updates_ftp_by_hostname(hostname))

        return rules


    def _iptables_updates_yum_fedora(self):

        rules = list()
        hostnames_http = list()
        ipaddrs_http = list()

        _logger.debug('{0}: Adding iptables rules for updates of yum for Fedora'.format(self.get_name()))


        repofiles = glob.glob(u'/etc/yum.repos.d/*.repo')
        for repofile in repofiles :
            Config = ConfigParser.ConfigParser()
            if Config.read(repofile) :
                sections = Config.sections()
                for section in sections :
                    if Config.has_option(section, u'enabled') :
                        enabled = Config.getint(section, u'enabled')
                    else :
                        enabled = 1

                    if enabled == 1 :
                        if Config.has_option(section, u'metalink') :
                            metalink = Config.get(section, u'metalink')
                            if u'http://' in metalink.lower() :
                                hostname = metalink.split(u'http://')[1].split(u'/')[0]
                                rules.append(self._iptables_updates_http_by_hostname(hostname))
                            elif u'https://' in metalink.lower() :
                                hostname = metalink.split(u'https://')[1].split(u'/')[0]
                                rules.append(self._iptables_updates_http_by_hostname(hostname))

                            urls = list()
                            urls = self._metalink_to_urls_resolve(metalink)
                            for url in urls :
                                if url.strip().startswith(u'http://') :
                                    hostname = url.split(u'http://')[1].split(u'/')[0]
                                    rules.append(self._iptables_updates_http_by_hostname(hostname))
                                elif url.strip().startswith(u'https://') :
                                    hostname = url.split(u'https://')[1].split(u'/')[0]
                                    rules.append(self._iptables_updates_https_by_hostname(hostname))
                                elif url.strip().startswith(u'ftp://') :
                                    if self._disable_auto_updates_ftp == False :
                                        hostname = url.split(u'ftp://')[1].split(u'/')[0]
                                        rules.append(self._iptables_updates_ftp_by_hostname(hostname))
                                elif url.strip().startswith(u'rsync://') :
                                    if self._disable_auto_updates_rsync == False :
                                        hostname = url.split(u'rsync://')[1].split(u'/')[0]
                                        rules.append(self._iptables_updates_rsync_by_hostname(hostname))

                        elif Config.has_option(section, u'baseurl') :
                            baseurl = Config.get(section, u'baseurl')
                            if baseurl.strip().startswith(u'http://') :
                                hostname = baseurl.split(u'http://')[1].split(u'/')[0]
                                rules.append(self._iptables_updates_http_by_hostname(hostname))
                            elif baseurl.strip().startswith(u'https://') :
                                hostname = baseurl.split(u'https://')[1].split(u'/')[0]
                                rules.append(self._iptables_updates_https_by_hostname(hostname))
                            elif baseurl.strip().startswith(u'ftp://') :
                                if self._disable_auto_updates_ftp == False :
                                    hostname = baseurl.split(u'ftp://')[1].split(u'/')[0]
                                    rules.append(self._iptables_updates_ftp_by_hostname(hostname))
                            elif url.strip().startswith(u'rsync://') :
                                if self._disable_auto_updates_rsync == False :
                                    hostname = url.split(u'rsync://')[1].split(u'/')[0]
                                    rules.append(self._iptables_updates_rsync_by_hostname(hostname))

        return rules


    def _hostname_to_ip_resolve(self, hostname, port):

        ipaddrs = list()

        if hostname :
            if port :
                if port > 0 and port < 65536 :
                    ais = socket.getaddrinfo(hostname, port, 0, 0, socket.IPPROTO_TCP)
                    for result in ais:
                        ipaddr = result[-1][0]
                        ipaddrs.append(ipaddr)

        return ipaddrs


    def _iptables_updates_http_by_hostname(self, hostname):

        rules = list()
        ipaddrs = list()

        if hostname :
            if hostname not in self._hostnames_http :
                if hostname.find(u':') == -1 :
                    self._hostnames_http.append(hostname)
                    ipaddrs = self._hostname_to_ip_resolve(hostname, 80)
                    for ipaddr in ipaddrs :
                        if ipaddr not in self._ipaddrs_http :
                            self._ipaddrs_http.append(ipaddr)
                            _logger.debug('{0}: adding System Update hostname: {1}, ip address: {2}, port: {3}'.format(self.get_name(), hostname, ipaddr, 80))
                            rules.append(create_iptables_egress_ingress_rule(ipaddr, 80, u'tcp', self._slot, transport=ipt.TRANSPORT_AUTO))
                else :
                    if hostname not in self._hostnames_special :
                        self._hostnames_special.append(hostname)
                        port = int(hostname.split(u':')[1])
                        hostname = hostname.split(u':')[0]
                        ipaddrs = self._hostname_to_ip_resolve(hostname, port)
                        for ipaddr in ipaddrs :
                            _logger.debug('{0}: adding System Update hostname: {1}, ip address: {2}, port: {3}'.format(self.get_name(), hostname, ipaddr, port))
                            rules.append(create_iptables_egress_ingress_rule(ipaddr, port, u'tcp', self._slot, transport=ipt.TRANSPORT_AUTO))

        return rules


    def _iptables_updates_https_by_hostname(self, hostname):

        rules = list()
        ipaddrs = list()

        if hostname :
            if hostname not in self._hostnames_https :
                if hostname.find(u':') == -1 :
                    self._hostnames_https.append(hostname)
                    ipaddrs = self._hostname_to_ip_resolve(hostname, 443)
                    for ipaddr in ipaddrs :
                        if ipaddr not in self._ipaddrs_https :
                            self._ipaddrs_https.append(ipaddr)
                            _logger.debug('{0}: adding System Update hostname: {1}, ip address: {2}, port: {3}'.format(self.get_name(), hostname, ipaddr, 443))
                            rules.append(create_iptables_egress_ingress_rule(ipaddr, 443, u'tcp', self._slot, transport=ipt.TRANSPORT_AUTO))
                else :
                    if hostname not in self._hostnames_special :
                        self._hostnames_special.append(hostname)
                        port = int(hostname.split(u':')[1])
                        hostname = hostname.split(u':')[0]
                        ipaddrs = self._hostname_to_ip_resolve(hostname, port)
                        for ipaddr in ipaddrs :
                            _logger.debug('{0}: adding System Update hostname: {1}, ip address: {2}, port: {3}'.format(self.get_name(), hostname, ipaddr, port))
                            rules.append(create_iptables_egress_ingress_rule(ipaddr, port, u'tcp', self._slot, transport=ipt.TRANSPORT_AUTO))

        return rules


    def _iptables_updates_ftp_by_hostname(self, hostname):

        rules = list()
        ipaddrs = list()

        if hostname :
            if hostname not in self._hostnames_ftp :
                self._hostnames_ftp.append(hostname)
                ipaddrs = self._hostname_to_ip_resolve(hostname, 21)
                for ipaddr in ipaddrs :
                    if ipaddr not in self._ipaddrs_ftp :
                        self._ipaddrs_ftp.append(ipaddr)
                        _logger.debug('{0}: adding System Update hostname: {1}, ip address: {2}, ftp ports: 21, 20, etc'.format(self.get_name(), hostname, ipaddr))
                        # FTP control
                        rules.append(create_iptables_egress_ingress_rule(ipaddr, 21, u'tcp', self._slot, transport=ipt.TRANSPORT_AUTO))
                        # FTP data transfer
                        rules.append(create_iptables_egress_rule_dest(ipaddr, 20, u'tcp', self._slot, u'ESTABLISHED', transport=ipt.TRANSPORT_AUTO))
                        rules.append(create_iptables_ingress_rule_source(ipaddr, 20, u'tcp', self._slot, u'ESTABLISHED,RELATED', transport=ipt.TRANSPORT_AUTO))
                        rules.append(create_iptables_egress_rule_dest(ipaddr, None, u'tcp', self._slot, u'ESTABLISHED,RELATED', transport=ipt.TRANSPORT_AUTO))
                        rules.append(create_iptables_ingress_rule_source(ipaddr, None, u'tcp', self._slot, u'ESTABLISHED', transport=ipt.TRANSPORT_AUTO))

        return rules


    def _iptables_updates_rsync_by_hostname(self, hostname):

        rules = list()
        ipaddrs = list()

        if hostname :
            if hostname not in self._hostnames_rsync :
                if hostname.find(u':') == -1 :
                    self._hostnames_rsync.append(hostname)
                    ipaddrs = self._hostname_to_ip_resolve(hostname, 873)
                    for ipaddr in ipaddrs :
                        if ipaddr not in self._ipaddrs_rsync :
                            self._ipaddrs_rsync.append(ipaddr)
                            _logger.debug('{0}: adding System Update hostname: {1}, ip address: {2}, port: {3}'.format(self.get_name(), hostname, ipaddr, 873))
                            rules.append(create_iptables_egress_ingress_rule(ipaddr, 873, u'tcp', self._slot, transport=ipt.TRANSPORT_AUTO))
                else :
                    if hostname not in self._hostnames_special :
                        self._hostnames_special.append(hostname)
                        port = int(hostname.split(u':')[1])
                        hostname = hostname.split(u':')[0]
                        ipaddrs = self._hostname_to_ip_resolve(hostname, port)
                        for ipaddr in ipaddrs :
                            _logger.debug('{0}: adding System Update hostname: {1}, ip address: {2}, port: {3}'.format(self.get_name(), hostname, ipaddr, port))
                            rules.append(create_iptables_egress_ingress_rule(ipaddr, port, u'tcp', self._slot, transport=ipt.TRANSPORT_AUTO))

        return rules


    def _mirrorlist_to_urls_resolve(self, mirrorlist):

        urls = list()

        if mirrorlist :
            mirrorlist = mirrorlist.replace(u'$releasever', self._dist_version)
            mirrorlist = mirrorlist.replace(u'$basearch', self._machine)
            mirrorlist = mirrorlist.replace(u'&infra=$infra', u'')

            storage = StringIO()
            c = pycurl.Curl()
            c.setopt(c.URL, mirrorlist.encode(u'utf-8'))
            c.setopt(c.WRITEFUNCTION, storage.write)
            c.perform()
            c.close()
            content = storage.getvalue()
            urls = content.split(u'\n')

        return urls


    def _metalink_to_urls_resolve(self, metalink):

        urls = list()

        if metalink :
            metalink = metalink.replace(u'$releasever', self._dist_version)
            metalink = metalink.replace(u'$basearch', self._machine)

            storage = StringIO()
            c = pycurl.Curl()
            c.setopt(c.URL, metalink.encode(u'utf-8'))
            c.setopt(c.WRITEFUNCTION, storage.write)
            c.perform()
            c.close()
            content = storage.getvalue()

            lines = content.split(u'\n')
            for line in lines :
                if line.find(u'<url protocol=') != -1 :
                    url = line.split(u' >')[1].split(u'</url>')[0]
                    urls.append(url)
                if line.find(u'xmlns="') != -1 :
                    url = line.split(u'xmlns="')[1].split(u'"')[0]
                    urls.append(url)
                if line.find(u'xmlns:mm0="') != -1 :
                    url = line.split(u'xmlns:mm0="')[1].split(u'"')[0]
                    urls.append(url)

        return urls
