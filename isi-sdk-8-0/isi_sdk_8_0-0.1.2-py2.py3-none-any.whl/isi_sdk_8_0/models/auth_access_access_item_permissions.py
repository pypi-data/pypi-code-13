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


class AuthAccessAccessItemPermissions(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AuthAccessAccessItemPermissions - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'dacl': 'str',
            'delete_child': 'str',
            'expected': 'str',
            'ownership': 'str',
            'sticky': 'str'
        }

        self.attribute_map = {
            'dacl': 'dacl',
            'delete_child': 'delete_child',
            'expected': 'expected',
            'ownership': 'ownership',
            'sticky': 'sticky'
        }

        self._dacl = None
        self._delete_child = None
        self._expected = None
        self._ownership = None
        self._sticky = None

    @property
    def dacl(self):
        """
        Gets the dacl of this AuthAccessAccessItemPermissions.
        Returns a status message if the Null ACL is set.

        :return: The dacl of this AuthAccessAccessItemPermissions.
        :rtype: str
        """
        return self._dacl

    @dacl.setter
    def dacl(self, dacl):
        """
        Sets the dacl of this AuthAccessAccessItemPermissions.
        Returns a status message if the Null ACL is set.

        :param dacl: The dacl of this AuthAccessAccessItemPermissions.
        :type: str
        """
        
        self._dacl = dacl

    @property
    def delete_child(self):
        """
        Gets the delete_child of this AuthAccessAccessItemPermissions.
        Returns a status message if the parent directory has the delete_child property set for the user. If the delete_child property is set for a user, that user is able to delete the file.the delete_child for the user.

        :return: The delete_child of this AuthAccessAccessItemPermissions.
        :rtype: str
        """
        return self._delete_child

    @delete_child.setter
    def delete_child(self, delete_child):
        """
        Sets the delete_child of this AuthAccessAccessItemPermissions.
        Returns a status message if the parent directory has the delete_child property set for the user. If the delete_child property is set for a user, that user is able to delete the file.the delete_child for the user.

        :param delete_child: The delete_child of this AuthAccessAccessItemPermissions.
        :type: str
        """
        
        self._delete_child = delete_child

    @property
    def expected(self):
        """
        Gets the expected of this AuthAccessAccessItemPermissions.
        Specifies the Access Control Entity (ACE) for the user.

        :return: The expected of this AuthAccessAccessItemPermissions.
        :rtype: str
        """
        return self._expected

    @expected.setter
    def expected(self, expected):
        """
        Sets the expected of this AuthAccessAccessItemPermissions.
        Specifies the Access Control Entity (ACE) for the user.

        :param expected: The expected of this AuthAccessAccessItemPermissions.
        :type: str
        """
        
        self._expected = expected

    @property
    def ownership(self):
        """
        Gets the ownership of this AuthAccessAccessItemPermissions.
        Returns a status message if the user owns the file.

        :return: The ownership of this AuthAccessAccessItemPermissions.
        :rtype: str
        """
        return self._ownership

    @ownership.setter
    def ownership(self, ownership):
        """
        Sets the ownership of this AuthAccessAccessItemPermissions.
        Returns a status message if the user owns the file.

        :param ownership: The ownership of this AuthAccessAccessItemPermissions.
        :type: str
        """
        
        self._ownership = ownership

    @property
    def sticky(self):
        """
        Gets the sticky of this AuthAccessAccessItemPermissions.
        Returns a status message if the user owns the file.

        :return: The sticky of this AuthAccessAccessItemPermissions.
        :rtype: str
        """
        return self._sticky

    @sticky.setter
    def sticky(self, sticky):
        """
        Sets the sticky of this AuthAccessAccessItemPermissions.
        Returns a status message if the user owns the file.

        :param sticky: The sticky of this AuthAccessAccessItemPermissions.
        :type: str
        """
        
        self._sticky = sticky

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

