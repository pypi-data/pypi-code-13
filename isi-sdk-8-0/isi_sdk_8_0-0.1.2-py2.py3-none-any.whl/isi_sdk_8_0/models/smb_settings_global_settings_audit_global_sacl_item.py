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


class SmbSettingsGlobalSettingsAuditGlobalSaclItem(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        SmbSettingsGlobalSettingsAuditGlobalSaclItem - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'flags': 'str',
            'permission': 'list[str]'
        }

        self.attribute_map = {
            'flags': 'flags',
            'permission': 'permission'
        }

        self._flags = None
        self._permission = None

    @property
    def flags(self):
        """
        Gets the flags of this SmbSettingsGlobalSettingsAuditGlobalSaclItem.
        Determines if audit is performed on success or failure.

        :return: The flags of this SmbSettingsGlobalSettingsAuditGlobalSaclItem.
        :rtype: str
        """
        return self._flags

    @flags.setter
    def flags(self, flags):
        """
        Sets the flags of this SmbSettingsGlobalSettingsAuditGlobalSaclItem.
        Determines if audit is performed on success or failure.

        :param flags: The flags of this SmbSettingsGlobalSettingsAuditGlobalSaclItem.
        :type: str
        """
        allowed_values = ["successful", "failed"]
        if flags not in allowed_values:
            raise ValueError(
                "Invalid value for `flags`, must be one of {0}"
                .format(allowed_values)
            )

        self._flags = flags

    @property
    def permission(self):
        """
        Gets the permission of this SmbSettingsGlobalSettingsAuditGlobalSaclItem.
        Specifies the array of filesystem rights that are governed.

        :return: The permission of this SmbSettingsGlobalSettingsAuditGlobalSaclItem.
        :rtype: list[str]
        """
        return self._permission

    @permission.setter
    def permission(self, permission):
        """
        Sets the permission of this SmbSettingsGlobalSettingsAuditGlobalSaclItem.
        Specifies the array of filesystem rights that are governed.

        :param permission: The permission of this SmbSettingsGlobalSettingsAuditGlobalSaclItem.
        :type: list[str]
        """
        
        self._permission = permission

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

