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


class SettingsKrb5Realm(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        SettingsKrb5Realm - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'admin_server': 'str',
            'default_domain': 'str',
            'is_default_realm': 'bool',
            'kdc': 'list[str]'
        }

        self.attribute_map = {
            'admin_server': 'admin_server',
            'default_domain': 'default_domain',
            'is_default_realm': 'is_default_realm',
            'kdc': 'kdc'
        }

        self._admin_server = None
        self._default_domain = None
        self._is_default_realm = None
        self._kdc = None

    @property
    def admin_server(self):
        """
        Gets the admin_server of this SettingsKrb5Realm.
        Specifies the administrative server hostname.

        :return: The admin_server of this SettingsKrb5Realm.
        :rtype: str
        """
        return self._admin_server

    @admin_server.setter
    def admin_server(self, admin_server):
        """
        Sets the admin_server of this SettingsKrb5Realm.
        Specifies the administrative server hostname.

        :param admin_server: The admin_server of this SettingsKrb5Realm.
        :type: str
        """
        
        self._admin_server = admin_server

    @property
    def default_domain(self):
        """
        Gets the default_domain of this SettingsKrb5Realm.
        Specifies the default domain mapped to the realm.

        :return: The default_domain of this SettingsKrb5Realm.
        :rtype: str
        """
        return self._default_domain

    @default_domain.setter
    def default_domain(self, default_domain):
        """
        Sets the default_domain of this SettingsKrb5Realm.
        Specifies the default domain mapped to the realm.

        :param default_domain: The default_domain of this SettingsKrb5Realm.
        :type: str
        """
        
        self._default_domain = default_domain

    @property
    def is_default_realm(self):
        """
        Gets the is_default_realm of this SettingsKrb5Realm.
        If true, indicates that the realm is the default.

        :return: The is_default_realm of this SettingsKrb5Realm.
        :rtype: bool
        """
        return self._is_default_realm

    @is_default_realm.setter
    def is_default_realm(self, is_default_realm):
        """
        Sets the is_default_realm of this SettingsKrb5Realm.
        If true, indicates that the realm is the default.

        :param is_default_realm: The is_default_realm of this SettingsKrb5Realm.
        :type: bool
        """
        
        self._is_default_realm = is_default_realm

    @property
    def kdc(self):
        """
        Gets the kdc of this SettingsKrb5Realm.
        Specifies the list of KDC hostnames.

        :return: The kdc of this SettingsKrb5Realm.
        :rtype: list[str]
        """
        return self._kdc

    @kdc.setter
    def kdc(self, kdc):
        """
        Sets the kdc of this SettingsKrb5Realm.
        Specifies the list of KDC hostnames.

        :param kdc: The kdc of this SettingsKrb5Realm.
        :type: list[str]
        """
        
        self._kdc = kdc

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

