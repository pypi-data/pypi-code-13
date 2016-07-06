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


class NodeStatusNodePowersupplies(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        NodeStatusNodePowersupplies - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'count': 'int',
            'failures': 'int',
            'has_cff': 'bool',
            'status': 'str',
            'supplies': 'list[NodeStatusNodePowersuppliesSupply]',
            'supports_cff': 'bool'
        }

        self.attribute_map = {
            'count': 'count',
            'failures': 'failures',
            'has_cff': 'has_cff',
            'status': 'status',
            'supplies': 'supplies',
            'supports_cff': 'supports_cff'
        }

        self._count = None
        self._failures = None
        self._has_cff = None
        self._status = None
        self._supplies = None
        self._supports_cff = None

    @property
    def count(self):
        """
        Gets the count of this NodeStatusNodePowersupplies.
        Count of how many power supplies are supported.

        :return: The count of this NodeStatusNodePowersupplies.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """
        Sets the count of this NodeStatusNodePowersupplies.
        Count of how many power supplies are supported.

        :param count: The count of this NodeStatusNodePowersupplies.
        :type: int
        """
        
        self._count = count

    @property
    def failures(self):
        """
        Gets the failures of this NodeStatusNodePowersupplies.
        Count of how many power supplies have failed.

        :return: The failures of this NodeStatusNodePowersupplies.
        :rtype: int
        """
        return self._failures

    @failures.setter
    def failures(self, failures):
        """
        Sets the failures of this NodeStatusNodePowersupplies.
        Count of how many power supplies have failed.

        :param failures: The failures of this NodeStatusNodePowersupplies.
        :type: int
        """
        
        self._failures = failures

    @property
    def has_cff(self):
        """
        Gets the has_cff of this NodeStatusNodePowersupplies.
        Does this node have a CFF power supply.

        :return: The has_cff of this NodeStatusNodePowersupplies.
        :rtype: bool
        """
        return self._has_cff

    @has_cff.setter
    def has_cff(self, has_cff):
        """
        Sets the has_cff of this NodeStatusNodePowersupplies.
        Does this node have a CFF power supply.

        :param has_cff: The has_cff of this NodeStatusNodePowersupplies.
        :type: bool
        """
        
        self._has_cff = has_cff

    @property
    def status(self):
        """
        Gets the status of this NodeStatusNodePowersupplies.
        A descriptive status string for this node's power supplies.

        :return: The status of this NodeStatusNodePowersupplies.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this NodeStatusNodePowersupplies.
        A descriptive status string for this node's power supplies.

        :param status: The status of this NodeStatusNodePowersupplies.
        :type: str
        """
        
        self._status = status

    @property
    def supplies(self):
        """
        Gets the supplies of this NodeStatusNodePowersupplies.
        List of this node's power supplies.

        :return: The supplies of this NodeStatusNodePowersupplies.
        :rtype: list[NodeStatusNodePowersuppliesSupply]
        """
        return self._supplies

    @supplies.setter
    def supplies(self, supplies):
        """
        Sets the supplies of this NodeStatusNodePowersupplies.
        List of this node's power supplies.

        :param supplies: The supplies of this NodeStatusNodePowersupplies.
        :type: list[NodeStatusNodePowersuppliesSupply]
        """
        
        self._supplies = supplies

    @property
    def supports_cff(self):
        """
        Gets the supports_cff of this NodeStatusNodePowersupplies.
        Does this node support CFF power supplies.

        :return: The supports_cff of this NodeStatusNodePowersupplies.
        :rtype: bool
        """
        return self._supports_cff

    @supports_cff.setter
    def supports_cff(self, supports_cff):
        """
        Sets the supports_cff of this NodeStatusNodePowersupplies.
        Does this node support CFF power supplies.

        :param supports_cff: The supports_cff of this NodeStatusNodePowersupplies.
        :type: bool
        """
        
        self._supports_cff = supports_cff

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

