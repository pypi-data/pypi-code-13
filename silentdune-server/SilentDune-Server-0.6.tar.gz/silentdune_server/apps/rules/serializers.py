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
from apps.rules.models import *


class BundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bundle
        fields = ('id', 'platform', 'name', 'descr', 'notes', 'default')


class RulePlatformListSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=50)
    desc = serializers.CharField(max_length=50)


class MachineSubsetSlotsListSerializer(serializers.Serializer):

    code = serializers.IntegerField()
    desc = serializers.CharField(max_length=50)
