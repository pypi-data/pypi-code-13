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


class ClusterOwner(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ClusterOwner - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'company': 'str',
            'location': 'str',
            'primary_email': 'str',
            'primary_name': 'str',
            'primary_phone1': 'str',
            'primary_phone2': 'str',
            'secondary_email': 'str',
            'secondary_name': 'str',
            'secondary_phone1': 'str',
            'secondary_phone2': 'str'
        }

        self.attribute_map = {
            'company': 'company',
            'location': 'location',
            'primary_email': 'primary_email',
            'primary_name': 'primary_name',
            'primary_phone1': 'primary_phone1',
            'primary_phone2': 'primary_phone2',
            'secondary_email': 'secondary_email',
            'secondary_name': 'secondary_name',
            'secondary_phone1': 'secondary_phone1',
            'secondary_phone2': 'secondary_phone2'
        }

        self._company = None
        self._location = None
        self._primary_email = None
        self._primary_name = None
        self._primary_phone1 = None
        self._primary_phone2 = None
        self._secondary_email = None
        self._secondary_name = None
        self._secondary_phone1 = None
        self._secondary_phone2 = None

    @property
    def company(self):
        """
        Gets the company of this ClusterOwner.
        Cluster owner company name.

        :return: The company of this ClusterOwner.
        :rtype: str
        """
        return self._company

    @company.setter
    def company(self, company):
        """
        Sets the company of this ClusterOwner.
        Cluster owner company name.

        :param company: The company of this ClusterOwner.
        :type: str
        """
        
        self._company = company

    @property
    def location(self):
        """
        Gets the location of this ClusterOwner.
        Cluster owner location.

        :return: The location of this ClusterOwner.
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """
        Sets the location of this ClusterOwner.
        Cluster owner location.

        :param location: The location of this ClusterOwner.
        :type: str
        """
        
        self._location = location

    @property
    def primary_email(self):
        """
        Gets the primary_email of this ClusterOwner.
        Cluster owner primary email address.

        :return: The primary_email of this ClusterOwner.
        :rtype: str
        """
        return self._primary_email

    @primary_email.setter
    def primary_email(self, primary_email):
        """
        Sets the primary_email of this ClusterOwner.
        Cluster owner primary email address.

        :param primary_email: The primary_email of this ClusterOwner.
        :type: str
        """
        
        self._primary_email = primary_email

    @property
    def primary_name(self):
        """
        Gets the primary_name of this ClusterOwner.
        Cluster owner primary contact name.

        :return: The primary_name of this ClusterOwner.
        :rtype: str
        """
        return self._primary_name

    @primary_name.setter
    def primary_name(self, primary_name):
        """
        Sets the primary_name of this ClusterOwner.
        Cluster owner primary contact name.

        :param primary_name: The primary_name of this ClusterOwner.
        :type: str
        """
        
        self._primary_name = primary_name

    @property
    def primary_phone1(self):
        """
        Gets the primary_phone1 of this ClusterOwner.
        Cluster owner primary contact phone number 1.

        :return: The primary_phone1 of this ClusterOwner.
        :rtype: str
        """
        return self._primary_phone1

    @primary_phone1.setter
    def primary_phone1(self, primary_phone1):
        """
        Sets the primary_phone1 of this ClusterOwner.
        Cluster owner primary contact phone number 1.

        :param primary_phone1: The primary_phone1 of this ClusterOwner.
        :type: str
        """
        
        self._primary_phone1 = primary_phone1

    @property
    def primary_phone2(self):
        """
        Gets the primary_phone2 of this ClusterOwner.
        Cluster owner primary contact phone number 2.

        :return: The primary_phone2 of this ClusterOwner.
        :rtype: str
        """
        return self._primary_phone2

    @primary_phone2.setter
    def primary_phone2(self, primary_phone2):
        """
        Sets the primary_phone2 of this ClusterOwner.
        Cluster owner primary contact phone number 2.

        :param primary_phone2: The primary_phone2 of this ClusterOwner.
        :type: str
        """
        
        self._primary_phone2 = primary_phone2

    @property
    def secondary_email(self):
        """
        Gets the secondary_email of this ClusterOwner.
        Cluster owner secondary email address.

        :return: The secondary_email of this ClusterOwner.
        :rtype: str
        """
        return self._secondary_email

    @secondary_email.setter
    def secondary_email(self, secondary_email):
        """
        Sets the secondary_email of this ClusterOwner.
        Cluster owner secondary email address.

        :param secondary_email: The secondary_email of this ClusterOwner.
        :type: str
        """
        
        self._secondary_email = secondary_email

    @property
    def secondary_name(self):
        """
        Gets the secondary_name of this ClusterOwner.
        Cluster owner secondary contact name.

        :return: The secondary_name of this ClusterOwner.
        :rtype: str
        """
        return self._secondary_name

    @secondary_name.setter
    def secondary_name(self, secondary_name):
        """
        Sets the secondary_name of this ClusterOwner.
        Cluster owner secondary contact name.

        :param secondary_name: The secondary_name of this ClusterOwner.
        :type: str
        """
        
        self._secondary_name = secondary_name

    @property
    def secondary_phone1(self):
        """
        Gets the secondary_phone1 of this ClusterOwner.
        Cluster owner secondary contact phone number 1.

        :return: The secondary_phone1 of this ClusterOwner.
        :rtype: str
        """
        return self._secondary_phone1

    @secondary_phone1.setter
    def secondary_phone1(self, secondary_phone1):
        """
        Sets the secondary_phone1 of this ClusterOwner.
        Cluster owner secondary contact phone number 1.

        :param secondary_phone1: The secondary_phone1 of this ClusterOwner.
        :type: str
        """
        
        self._secondary_phone1 = secondary_phone1

    @property
    def secondary_phone2(self):
        """
        Gets the secondary_phone2 of this ClusterOwner.
        Cluster owner secondary contact phone number 2.

        :return: The secondary_phone2 of this ClusterOwner.
        :rtype: str
        """
        return self._secondary_phone2

    @secondary_phone2.setter
    def secondary_phone2(self, secondary_phone2):
        """
        Sets the secondary_phone2 of this ClusterOwner.
        Cluster owner secondary contact phone number 2.

        :param secondary_phone2: The secondary_phone2 of this ClusterOwner.
        :type: str
        """
        
        self._secondary_phone2 = secondary_phone2

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

