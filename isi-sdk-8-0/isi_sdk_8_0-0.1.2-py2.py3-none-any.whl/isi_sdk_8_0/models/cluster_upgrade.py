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


class ClusterUpgrade(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ClusterUpgrade - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'nodes_to_rolling_upgrade': 'list[int]'
        }

        self.attribute_map = {
            'nodes_to_rolling_upgrade': 'nodes_to_rolling_upgrade'
        }

        self._nodes_to_rolling_upgrade = None

    @property
    def nodes_to_rolling_upgrade(self):
        """
        Gets the nodes_to_rolling_upgrade of this ClusterUpgrade.
        The nodes (to be) scheduled for an existing upgrade ordered by queue position number. [<lnn-1>, <lnn-2>, ... ], 'All', null

        :return: The nodes_to_rolling_upgrade of this ClusterUpgrade.
        :rtype: list[int]
        """
        return self._nodes_to_rolling_upgrade

    @nodes_to_rolling_upgrade.setter
    def nodes_to_rolling_upgrade(self, nodes_to_rolling_upgrade):
        """
        Sets the nodes_to_rolling_upgrade of this ClusterUpgrade.
        The nodes (to be) scheduled for an existing upgrade ordered by queue position number. [<lnn-1>, <lnn-2>, ... ], 'All', null

        :param nodes_to_rolling_upgrade: The nodes_to_rolling_upgrade of this ClusterUpgrade.
        :type: list[int]
        """
        
        self._nodes_to_rolling_upgrade = nodes_to_rolling_upgrade

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

