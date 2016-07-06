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


class AuthRoleExtended(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AuthRoleExtended - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'description': 'str',
            'members': 'list[GroupMember]',
            'name': 'str',
            'privileges': 'list[AuthIdNtokenPrivilegeItem]',
            'id': 'str'
        }

        self.attribute_map = {
            'description': 'description',
            'members': 'members',
            'name': 'name',
            'privileges': 'privileges',
            'id': 'id'
        }

        self._description = None
        self._members = None
        self._name = None
        self._privileges = None
        self._id = None

    @property
    def description(self):
        """
        Gets the description of this AuthRoleExtended.
        Specifies the description of the role.

        :return: The description of this AuthRoleExtended.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this AuthRoleExtended.
        Specifies the description of the role.

        :param description: The description of this AuthRoleExtended.
        :type: str
        """
        
        self._description = description

    @property
    def members(self):
        """
        Gets the members of this AuthRoleExtended.
        Specifies the users or groups that have this role.

        :return: The members of this AuthRoleExtended.
        :rtype: list[GroupMember]
        """
        return self._members

    @members.setter
    def members(self, members):
        """
        Sets the members of this AuthRoleExtended.
        Specifies the users or groups that have this role.

        :param members: The members of this AuthRoleExtended.
        :type: list[GroupMember]
        """
        
        self._members = members

    @property
    def name(self):
        """
        Gets the name of this AuthRoleExtended.
        Specifies the name of the role.

        :return: The name of this AuthRoleExtended.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this AuthRoleExtended.
        Specifies the name of the role.

        :param name: The name of this AuthRoleExtended.
        :type: str
        """
        
        self._name = name

    @property
    def privileges(self):
        """
        Gets the privileges of this AuthRoleExtended.
        Specifies the privileges granted by this role.

        :return: The privileges of this AuthRoleExtended.
        :rtype: list[AuthIdNtokenPrivilegeItem]
        """
        return self._privileges

    @privileges.setter
    def privileges(self, privileges):
        """
        Sets the privileges of this AuthRoleExtended.
        Specifies the privileges granted by this role.

        :param privileges: The privileges of this AuthRoleExtended.
        :type: list[AuthIdNtokenPrivilegeItem]
        """
        
        self._privileges = privileges

    @property
    def id(self):
        """
        Gets the id of this AuthRoleExtended.
        Specifies the ID of the role.

        :return: The id of this AuthRoleExtended.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AuthRoleExtended.
        Specifies the ID of the role.

        :param id: The id of this AuthRoleExtended.
        :type: str
        """
        
        self._id = id

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

