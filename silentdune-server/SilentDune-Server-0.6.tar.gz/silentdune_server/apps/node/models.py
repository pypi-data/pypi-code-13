#
# Authors: Robert Abram <robert.abram@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'COPYING' for use and warranty information
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

# The Models created here should apply to all firewall applications

from django.utils.translation import ugettext_lazy as _
from django.db import models
from proj.models import BaseModel
from apps.rules.models import Bundle
from apps.rules.models import RULE_PLATFORMS

# List of operating systems supported by this app
OS_PLATFORMS = (
    ('linux', 'Linux'),
)


# A Bundle Name record is what a client machine is linked with
class Node (BaseModel):

    # ** CHANGE LOCATIONS **
    #  NodeSerializer in app/node/seralizers.py
    #  BaseTest.setUp() in tests/base_api_test.py
    #  NodeProcessTestCase.test_api_node_post() in tests/test_oauth_auth.py
    #  silentdune_client.models.node.Node model in node.py

    platform = models.CharField(_('Firewall Platform'), max_length=30, choices=RULE_PLATFORMS, default='linux')
    os = models.CharField(_('OS Name'), max_length=30, choices=OS_PLATFORMS, default='')
    dist = models.CharField(_('Node Distribution'), max_length=100, default='')
    dist_version = models.CharField(_('Node Distribution Version'), max_length=50, default='')
    system = models.CharField(_('System'), max_length=256, default='')  # User defined. IE: Database Server
    hostname = models.CharField(_('Host name'), max_length=256, default='')
    python_version = models.CharField(_('Python Version'), max_length=256, default='')
    machine_id = models.CharField(_('Node Machine ID'), max_length=100, unique=True)
    active = models.BooleanField(_('Active'), default=False)
    locked = models.BooleanField(_('Locked'), default=False)
    last_connection = models.DateTimeField(_('Last Connection Timestamp'), auto_now_add=True)
    sync = models.BooleanField(_('Node Synchronized'), default=False)
    push = models.BooleanField(_('Push'), default=False)
    polling_interval = models.IntegerField(_('Polling Interval'), default=60)
    fernet_key = models.CharField(_('Fernet key'), max_length=64, default='')
    notes = models.CharField(_('Notes'), max_length=4000, default='', null=True, blank=True)  

    class Meta:
        db_table = 'node'


class NodeInterfaces (BaseModel):

    node = models.ForeignKey(Node)
    name = models.CharField(_('Interface Name'), max_length=256)
    uuid = models.CharField(_('Block ID'), max_length=64, null=True)
    interface_type = models.CharField(_('Interface Type'), max_length=256)
    device = models.CharField(_('Device Name'), max_length=256)
    active = models.BooleanField(_('Active'))
    ip_address = models.GenericIPAddressField(_('IP Address'), default='192.168.0.1')

    class Meta:
        db_table = 'node_interfaces'


class NodeBundle (BaseModel):

    node = models.OneToOneField(Node)
    bundle = models.ForeignKey(Bundle)

    class Meta:
        db_table = 'node_bundle'


class NodeProcess (BaseModel):

    # ** CHANGE LOCATIONS **
    #  NodeProcessSerializer in apps/node/seralizers.py
    #  NodeProcessViewSet in apps/node/views.py
    #  NodeProcessTestCase.test_node_process() in tests/test_node_processes.py
    #  silentdune_client.models.node.NodeProcess model in node.py

    node = models.ForeignKey(Node)
    pid = models.CharField(_('Process ID'), max_length=100)
    name = models.CharField(_('Process Name'), max_length=500)
    category = models.CharField(_('Process Type Category'), max_length=100, default='unknown')
    running = models.BooleanField(_('Running'))
    runningfor = models.CharField(_('Running For'), max_length=250)
    ipaddr = models.CharField(_('IP Addresses'), max_length=500, default='*')
    port = models.CharField(_('Port'), max_length=50, default='')
    lockable = models.BooleanField(_('Lockable'), default=False)
    locked = models.BooleanField(_('Locked'), default=True)
    delete = models.BooleanField(default=False)  # No UI

    class Meta:
        db_table = 'node_processes'
        unique_together = ('node', 'name', 'category')
