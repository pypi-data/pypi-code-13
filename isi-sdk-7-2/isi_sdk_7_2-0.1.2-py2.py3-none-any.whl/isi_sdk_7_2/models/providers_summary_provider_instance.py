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


class ProvidersSummaryProviderInstance(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ProvidersSummaryProviderInstance - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'active_server': 'str',
            'connections': 'list[ProvidersSummaryProviderInstanceConnection]',
            'forest': 'str',
            'id': 'str',
            'name': 'str',
            'site': 'str',
            'status': 'str',
            'type': 'str'
        }

        self.attribute_map = {
            'active_server': 'active_server',
            'connections': 'connections',
            'forest': 'forest',
            'id': 'id',
            'name': 'name',
            'site': 'site',
            'status': 'status',
            'type': 'type'
        }

        self._active_server = None
        self._connections = None
        self._forest = None
        self._id = None
        self._name = None
        self._site = None
        self._status = None
        self._type = None

    @property
    def active_server(self):
        """
        Gets the active_server of this ProvidersSummaryProviderInstance.
        The server the provider is using to serve authentication requests. Null if no server is set or is not applicable for that provider.

        :return: The active_server of this ProvidersSummaryProviderInstance.
        :rtype: str
        """
        return self._active_server

    @active_server.setter
    def active_server(self, active_server):
        """
        Sets the active_server of this ProvidersSummaryProviderInstance.
        The server the provider is using to serve authentication requests. Null if no server is set or is not applicable for that provider.

        :param active_server: The active_server of this ProvidersSummaryProviderInstance.
        :type: str
        """
        
        self._active_server = active_server

    @property
    def connections(self):
        """
        Gets the connections of this ProvidersSummaryProviderInstance.


        :return: The connections of this ProvidersSummaryProviderInstance.
        :rtype: list[ProvidersSummaryProviderInstanceConnection]
        """
        return self._connections

    @connections.setter
    def connections(self, connections):
        """
        Sets the connections of this ProvidersSummaryProviderInstance.


        :param connections: The connections of this ProvidersSummaryProviderInstance.
        :type: list[ProvidersSummaryProviderInstanceConnection]
        """
        
        self._connections = connections

    @property
    def forest(self):
        """
        Gets the forest of this ProvidersSummaryProviderInstance.
        The active directory forest. Null if not applicable.

        :return: The forest of this ProvidersSummaryProviderInstance.
        :rtype: str
        """
        return self._forest

    @forest.setter
    def forest(self, forest):
        """
        Sets the forest of this ProvidersSummaryProviderInstance.
        The active directory forest. Null if not applicable.

        :param forest: The forest of this ProvidersSummaryProviderInstance.
        :type: str
        """
        
        self._forest = forest

    @property
    def id(self):
        """
        Gets the id of this ProvidersSummaryProviderInstance.
        The ID of the provider.

        :return: The id of this ProvidersSummaryProviderInstance.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ProvidersSummaryProviderInstance.
        The ID of the provider.

        :param id: The id of this ProvidersSummaryProviderInstance.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ProvidersSummaryProviderInstance.
        The name of the provider.

        :return: The name of this ProvidersSummaryProviderInstance.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ProvidersSummaryProviderInstance.
        The name of the provider.

        :param name: The name of this ProvidersSummaryProviderInstance.
        :type: str
        """
        
        self._name = name

    @property
    def site(self):
        """
        Gets the site of this ProvidersSummaryProviderInstance.
        The active directory forest. Null if not applicable.

        :return: The site of this ProvidersSummaryProviderInstance.
        :rtype: str
        """
        return self._site

    @site.setter
    def site(self, site):
        """
        Sets the site of this ProvidersSummaryProviderInstance.
        The active directory forest. Null if not applicable.

        :param site: The site of this ProvidersSummaryProviderInstance.
        :type: str
        """
        
        self._site = site

    @property
    def status(self):
        """
        Gets the status of this ProvidersSummaryProviderInstance.
        The status of the provider.

        :return: The status of this ProvidersSummaryProviderInstance.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this ProvidersSummaryProviderInstance.
        The status of the provider.

        :param status: The status of this ProvidersSummaryProviderInstance.
        :type: str
        """
        allowed_values = ["offline", "active", "online", "initializing", "joining", "disabled"]
        if status is not None and status not in allowed_values:
            raise ValueError(
                "Invalid value for `status`, must be one of {0}"
                .format(allowed_values)
            )

        self._status = status

    @property
    def type(self):
        """
        Gets the type of this ProvidersSummaryProviderInstance.
        The type of provider.

        :return: The type of this ProvidersSummaryProviderInstance.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ProvidersSummaryProviderInstance.
        The type of provider.

        :param type: The type of this ProvidersSummaryProviderInstance.
        :type: str
        """
        allowed_values = ["file", "ldap", "local", "nis", "ads", "krb5", "unknown"]
        if type is not None and type not in allowed_values:
            raise ValueError(
                "Invalid value for `type`, must be one of {0}"
                .format(allowed_values)
            )

        self._type = type

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

