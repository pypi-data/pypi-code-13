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

from rest_framework import serializers
from apps.node.models import *


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('id', 'platform', 'os', 'dist', 'dist_version', 'hostname', 'python_version', 'machine_id',
                  'last_connection', 'sync', 'notes', 'active', 'locked', 'polling_interval', 'fernet_key')


class NodeNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('id', 'system', 'dist')


class NodeInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeInterfaces
        fields = ('id', 'node', 'name', 'uuid', 'type', 'device', 'active')


class NodeBundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeBundle
        fields = ('id', 'bundle', 'node')


class NodeProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeProcess
        fields = ('id', 'node', 'name', 'category', 'running', 'runningfor', 'ipaddr', 'port', 'lockable',
                  'locked', 'delete')
