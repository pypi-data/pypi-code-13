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
from apps.rules.iptables.models import *


class IPTransportVersionListSerializer(serializers.Serializer):

    code = serializers.IntegerField()
    desc = serializers.CharField(max_length=4)


class IPMatchOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPTablesMatchOptions
        fields = ('id', 'option', 'value', 'invert', 'sort_id')

        
class IPMatchSerializer(serializers.ModelSerializer):

    options = IPMatchOptionsSerializer(many=True)

    class Meta:
        model = IPTablesMatch
        fields = ('id', 'name', 'options', )


class IPJumpOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPTablesJumpOptions
        fields = ('id', 'name', 'value', )


class IPJumpSerializer(serializers.ModelSerializer):

    params = IPJumpOptionsSerializer(many=True)

    class Meta:
        model = IPTablesJump
        fields = ('id', 'target', 'params', )

                
class IPRuleSerializer(serializers.ModelSerializer):

    matches = IPMatchSerializer(many=True)
    jump = IPJumpSerializer()

    class Meta:
        model = IPTablesRule
        fields = ('id', 'enabled', 'sort_id', 'descr', 'ifacein_name', 'ifacein_invert',
                  'ifaceout_name', 'ifaceout_invert', 'ip_protocol_name', 'ip_protocol_invert',
                  'source_address', 'source_mask', 'source_invert', 'dest_address', 
                  'dest_mask', 'dest_invert', 'fragment', 'fragment_invert', 'matches', 'jump')


class IPRingSerializer(serializers.ModelSerializer):

    rules = IPRuleSerializer(many=True)

    class Meta:
        model = IPTablesRing
        fields = ('id', 'name', 'version', 'rules')


class IPChainSerializer(serializers.ModelSerializer):

    rings = IPRingSerializer(many=True)

    class Meta:
        model = IPTablesChain
        fields = ('id', 'name', 'rings')


class IPMachineSubsetSerializer(serializers.ModelSerializer):

    chains = IPChainSerializer(many=True)

    class Meta:
        model = IPTablesMachineSubset
        fields = ('id', 'name', 'descr', 'notes', 'platform', 'slot', 'sort_id', 'chains', 'active')


class IPMachineSubsetNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPTablesMachineSubset
        fields = ('id', 'name', 'descr')


class IPMachineSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPTablesMachineSet
        fields = ('id', 'machine_subset')
