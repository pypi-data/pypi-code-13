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


class ClusterAddNodeItem(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ClusterAddNodeItem - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'allow_down': 'bool',
            'serial_number': 'str',
            'skip_hardware_version_check': 'bool'
        }

        self.attribute_map = {
            'allow_down': 'allow_down',
            'serial_number': 'serial_number',
            'skip_hardware_version_check': 'skip_hardware_version_check'
        }

        self._allow_down = None
        self._serial_number = None
        self._skip_hardware_version_check = None

    @property
    def allow_down(self):
        """
        Gets the allow_down of this ClusterAddNodeItem.
        Allow down nodes (Default false).

        :return: The allow_down of this ClusterAddNodeItem.
        :rtype: bool
        """
        return self._allow_down

    @allow_down.setter
    def allow_down(self, allow_down):
        """
        Sets the allow_down of this ClusterAddNodeItem.
        Allow down nodes (Default false).

        :param allow_down: The allow_down of this ClusterAddNodeItem.
        :type: bool
        """
        
        self._allow_down = allow_down

    @property
    def serial_number(self):
        """
        Gets the serial_number of this ClusterAddNodeItem.
        Serial number of this node.

        :return: The serial_number of this ClusterAddNodeItem.
        :rtype: str
        """
        return self._serial_number

    @serial_number.setter
    def serial_number(self, serial_number):
        """
        Sets the serial_number of this ClusterAddNodeItem.
        Serial number of this node.

        :param serial_number: The serial_number of this ClusterAddNodeItem.
        :type: str
        """
        
        self._serial_number = serial_number

    @property
    def skip_hardware_version_check(self):
        """
        Gets the skip_hardware_version_check of this ClusterAddNodeItem.
        Bypass hardware version checks (Default false).

        :return: The skip_hardware_version_check of this ClusterAddNodeItem.
        :rtype: bool
        """
        return self._skip_hardware_version_check

    @skip_hardware_version_check.setter
    def skip_hardware_version_check(self, skip_hardware_version_check):
        """
        Sets the skip_hardware_version_check of this ClusterAddNodeItem.
        Bypass hardware version checks (Default false).

        :param skip_hardware_version_check: The skip_hardware_version_check of this ClusterAddNodeItem.
        :type: bool
        """
        
        self._skip_hardware_version_check = skip_hardware_version_check

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

