# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re


class SyncRule(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        SyncRule - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'description': 'str',
            'enabled': 'bool',
            'limit': 'int',
            'schedule': 'SyncRuleSchedule'
        }

        self.attribute_map = {
            'description': 'description',
            'enabled': 'enabled',
            'limit': 'limit',
            'schedule': 'schedule'
        }

        self._description = None
        self._enabled = None
        self._limit = None
        self._schedule = None

    @property
    def description(self):
        """
        Gets the description of this SyncRule.
        User-entered description of this performance rule.

        :return: The description of this SyncRule.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this SyncRule.
        User-entered description of this performance rule.

        :param description: The description of this SyncRule.
        :type: str
        """
        
        self._description = description

    @property
    def enabled(self):
        """
        Gets the enabled of this SyncRule.
        Whether this performance rule is currently in effect during its specified intervals.

        :return: The enabled of this SyncRule.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this SyncRule.
        Whether this performance rule is currently in effect during its specified intervals.

        :param enabled: The enabled of this SyncRule.
        :type: bool
        """
        
        self._enabled = enabled

    @property
    def limit(self):
        """
        Gets the limit of this SyncRule.
        Amount the specified system resource type is limited by this rule.  Units are kb/s for bandwidth, files/s for file-count, processing percentage used for cpu, or percentage of maximum available workers.

        :return: The limit of this SyncRule.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """
        Sets the limit of this SyncRule.
        Amount the specified system resource type is limited by this rule.  Units are kb/s for bandwidth, files/s for file-count, processing percentage used for cpu, or percentage of maximum available workers.

        :param limit: The limit of this SyncRule.
        :type: int
        """
        
        self._limit = limit

    @property
    def schedule(self):
        """
        Gets the schedule of this SyncRule.
        A schedule defining when during a week this performance rule is in effect.  If unspecified or null, the schedule will always be in effect.

        :return: The schedule of this SyncRule.
        :rtype: SyncRuleSchedule
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """
        Sets the schedule of this SyncRule.
        A schedule defining when during a week this performance rule is in effect.  If unspecified or null, the schedule will always be in effect.

        :param schedule: The schedule of this SyncRule.
        :type: SyncRuleSchedule
        """
        
        self._schedule = schedule

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

