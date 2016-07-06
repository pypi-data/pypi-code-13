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


class StoragepoolStatusUnprovisionedItem(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        StoragepoolStatusUnprovisionedItem - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'bay': 'int',
            'lnn': 'int'
        }

        self.attribute_map = {
            'bay': 'bay',
            'lnn': 'lnn'
        }

        self._bay = None
        self._lnn = None

    @property
    def bay(self):
        """
        Gets the bay of this StoragepoolStatusUnprovisionedItem.
        The drive bay number.

        :return: The bay of this StoragepoolStatusUnprovisionedItem.
        :rtype: int
        """
        return self._bay

    @bay.setter
    def bay(self, bay):
        """
        Sets the bay of this StoragepoolStatusUnprovisionedItem.
        The drive bay number.

        :param bay: The bay of this StoragepoolStatusUnprovisionedItem.
        :type: int
        """
        
        self._bay = bay

    @property
    def lnn(self):
        """
        Gets the lnn of this StoragepoolStatusUnprovisionedItem.
        The node the drive is on.

        :return: The lnn of this StoragepoolStatusUnprovisionedItem.
        :rtype: int
        """
        return self._lnn

    @lnn.setter
    def lnn(self, lnn):
        """
        Sets the lnn of this StoragepoolStatusUnprovisionedItem.
        The node the drive is on.

        :param lnn: The lnn of this StoragepoolStatusUnprovisionedItem.
        :type: int
        """
        
        self._lnn = lnn

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

