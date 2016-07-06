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


class TargetReportsExtended(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        TargetReportsExtended - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'reports': 'list[TargetReport]',
            'resume': 'str',
            'total': 'int'
        }

        self.attribute_map = {
            'reports': 'reports',
            'resume': 'resume',
            'total': 'total'
        }

        self._reports = None
        self._resume = None
        self._total = None

    @property
    def reports(self):
        """
        Gets the reports of this TargetReportsExtended.


        :return: The reports of this TargetReportsExtended.
        :rtype: list[TargetReport]
        """
        return self._reports

    @reports.setter
    def reports(self, reports):
        """
        Sets the reports of this TargetReportsExtended.


        :param reports: The reports of this TargetReportsExtended.
        :type: list[TargetReport]
        """
        
        self._reports = reports

    @property
    def resume(self):
        """
        Gets the resume of this TargetReportsExtended.
        Continue returning results from previous call using this token (token should come from the previous call, resume cannot be used with other options).

        :return: The resume of this TargetReportsExtended.
        :rtype: str
        """
        return self._resume

    @resume.setter
    def resume(self, resume):
        """
        Sets the resume of this TargetReportsExtended.
        Continue returning results from previous call using this token (token should come from the previous call, resume cannot be used with other options).

        :param resume: The resume of this TargetReportsExtended.
        :type: str
        """
        
        self._resume = resume

    @property
    def total(self):
        """
        Gets the total of this TargetReportsExtended.
        Total number of items available.

        :return: The total of this TargetReportsExtended.
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total):
        """
        Sets the total of this TargetReportsExtended.
        Total number of items available.

        :param total: The total of this TargetReportsExtended.
        :type: int
        """
        
        self._total = total

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

