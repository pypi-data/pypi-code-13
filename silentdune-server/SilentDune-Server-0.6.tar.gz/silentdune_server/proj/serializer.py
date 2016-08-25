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

# Note: IPTables serializers have been moved to apps.rules.iptables.serializers

from rest_framework import serializers
from django.contrib.auth.models import User, Group
from apps.accounts.models import UserProfile
from proj.models import GlobalPreferences


# Generic Serializer for Chooser Tuples
class ChooserListBaseSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=50)
    desc = serializers.CharField(max_length=50)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('accepted_terms', 'email_reg_code', 'account_activated', 'oauth_scope')


class UserSerializer(serializers.ModelSerializer):
    # profile = UserProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_superuser')


class GlobalPreferencesSerializer(serializers.ModelSerializer):

    class Meta:
        model = GlobalPreferences
        fields = ('lockdown_slot_level', 'polling_interval')


class UserNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class RecordCountSerializer(serializers.Serializer):
    data = serializers.ReadOnlyField()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')



