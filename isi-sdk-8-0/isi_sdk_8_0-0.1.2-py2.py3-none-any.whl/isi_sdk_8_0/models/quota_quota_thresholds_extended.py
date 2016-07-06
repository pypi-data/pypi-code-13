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


class QuotaQuotaThresholdsExtended(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        QuotaQuotaThresholdsExtended - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'advisory': 'int',
            'hard': 'int',
            'soft': 'int',
            'soft_grace': 'int',
            'advisory_exceeded': 'bool',
            'advisory_last_exceeded': 'int',
            'hard_exceeded': 'bool',
            'hard_last_exceeded': 'int',
            'soft_exceeded': 'bool',
            'soft_last_exceeded': 'int'
        }

        self.attribute_map = {
            'advisory': 'advisory',
            'hard': 'hard',
            'soft': 'soft',
            'soft_grace': 'soft_grace',
            'advisory_exceeded': 'advisory_exceeded',
            'advisory_last_exceeded': 'advisory_last_exceeded',
            'hard_exceeded': 'hard_exceeded',
            'hard_last_exceeded': 'hard_last_exceeded',
            'soft_exceeded': 'soft_exceeded',
            'soft_last_exceeded': 'soft_last_exceeded'
        }

        self._advisory = None
        self._hard = None
        self._soft = None
        self._soft_grace = None
        self._advisory_exceeded = None
        self._advisory_last_exceeded = None
        self._hard_exceeded = None
        self._hard_last_exceeded = None
        self._soft_exceeded = None
        self._soft_last_exceeded = None

    @property
    def advisory(self):
        """
        Gets the advisory of this QuotaQuotaThresholdsExtended.
        Usage bytes at which notifications will be sent but writes will not be denied.

        :return: The advisory of this QuotaQuotaThresholdsExtended.
        :rtype: int
        """
        return self._advisory

    @advisory.setter
    def advisory(self, advisory):
        """
        Sets the advisory of this QuotaQuotaThresholdsExtended.
        Usage bytes at which notifications will be sent but writes will not be denied.

        :param advisory: The advisory of this QuotaQuotaThresholdsExtended.
        :type: int
        """
        
        if advisory is not None and advisory < 1.0:
            raise ValueError("Invalid value for `advisory`, must be a value greater than or equal to `1.0`")

        self._advisory = advisory

    @property
    def hard(self):
        """
        Gets the hard of this QuotaQuotaThresholdsExtended.
        Usage bytes at which further writes will be denied.

        :return: The hard of this QuotaQuotaThresholdsExtended.
        :rtype: int
        """
        return self._hard

    @hard.setter
    def hard(self, hard):
        """
        Sets the hard of this QuotaQuotaThresholdsExtended.
        Usage bytes at which further writes will be denied.

        :param hard: The hard of this QuotaQuotaThresholdsExtended.
        :type: int
        """
        
        if hard is not None and hard < 1.0:
            raise ValueError("Invalid value for `hard`, must be a value greater than or equal to `1.0`")

        self._hard = hard

    @property
    def soft(self):
        """
        Gets the soft of this QuotaQuotaThresholdsExtended.
        Usage bytes at which notifications will be sent and soft grace time will be started.

        :return: The soft of this QuotaQuotaThresholdsExtended.
        :rtype: int
        """
        return self._soft

    @soft.setter
    def soft(self, soft):
        """
        Sets the soft of this QuotaQuotaThresholdsExtended.
        Usage bytes at which notifications will be sent and soft grace time will be started.

        :param soft: The soft of this QuotaQuotaThresholdsExtended.
        :type: int
        """
        
        if soft is not None and soft < 1.0:
            raise ValueError("Invalid value for `soft`, must be a value greater than or equal to `1.0`")

        self._soft = soft

    @property
    def soft_grace(self):
        """
        Gets the soft_grace of this QuotaQuotaThresholdsExtended.
        Time in seconds after which the soft threshold has been hit before writes will be denied.

        :return: The soft_grace of this QuotaQuotaThresholdsExtended.
        :rtype: int
        """
        return self._soft_grace

    @soft_grace.setter
    def soft_grace(self, soft_grace):
        """
        Sets the soft_grace of this QuotaQuotaThresholdsExtended.
        Time in seconds after which the soft threshold has been hit before writes will be denied.

        :param soft_grace: The soft_grace of this QuotaQuotaThresholdsExtended.
        :type: int
        """
        
        if soft_grace is not None and soft_grace < 1.0:
            raise ValueError("Invalid value for `soft_grace`, must be a value greater than or equal to `1.0`")

        self._soft_grace = soft_grace

    @property
    def advisory_exceeded(self):
        """
        Gets the advisory_exceeded of this QuotaQuotaThresholdsExtended.
        True if the advisory threshold has been hit.

        :return: The advisory_exceeded of this QuotaQuotaThresholdsExtended.
        :rtype: bool
        """
        return self._advisory_exceeded

    @advisory_exceeded.setter
    def advisory_exceeded(self, advisory_exceeded):
        """
        Sets the advisory_exceeded of this QuotaQuotaThresholdsExtended.
        True if the advisory threshold has been hit.

        :param advisory_exceeded: The advisory_exceeded of this QuotaQuotaThresholdsExtended.
        :type: bool
        """
        
        self._advisory_exceeded = advisory_exceeded

    @property
    def advisory_last_exceeded(self):
        """
        Gets the advisory_last_exceeded of this QuotaQuotaThresholdsExtended.
        Time at which advisory threshold was hit.

        :return: The advisory_last_exceeded of this QuotaQuotaThresholdsExtended.
        :rtype: int
        """
        return self._advisory_last_exceeded

    @advisory_last_exceeded.setter
    def advisory_last_exceeded(self, advisory_last_exceeded):
        """
        Sets the advisory_last_exceeded of this QuotaQuotaThresholdsExtended.
        Time at which advisory threshold was hit.

        :param advisory_last_exceeded: The advisory_last_exceeded of this QuotaQuotaThresholdsExtended.
        :type: int
        """
        
        self._advisory_last_exceeded = advisory_last_exceeded

    @property
    def hard_exceeded(self):
        """
        Gets the hard_exceeded of this QuotaQuotaThresholdsExtended.
        True if the hard threshold has been hit.

        :return: The hard_exceeded of this QuotaQuotaThresholdsExtended.
        :rtype: bool
        """
        return self._hard_exceeded

    @hard_exceeded.setter
    def hard_exceeded(self, hard_exceeded):
        """
        Sets the hard_exceeded of this QuotaQuotaThresholdsExtended.
        True if the hard threshold has been hit.

        :param hard_exceeded: The hard_exceeded of this QuotaQuotaThresholdsExtended.
        :type: bool
        """
        
        self._hard_exceeded = hard_exceeded

    @property
    def hard_last_exceeded(self):
        """
        Gets the hard_last_exceeded of this QuotaQuotaThresholdsExtended.
        Time at which hard threshold was hit.

        :return: The hard_last_exceeded of this QuotaQuotaThresholdsExtended.
        :rtype: int
        """
        return self._hard_last_exceeded

    @hard_last_exceeded.setter
    def hard_last_exceeded(self, hard_last_exceeded):
        """
        Sets the hard_last_exceeded of this QuotaQuotaThresholdsExtended.
        Time at which hard threshold was hit.

        :param hard_last_exceeded: The hard_last_exceeded of this QuotaQuotaThresholdsExtended.
        :type: int
        """
        
        self._hard_last_exceeded = hard_last_exceeded

    @property
    def soft_exceeded(self):
        """
        Gets the soft_exceeded of this QuotaQuotaThresholdsExtended.
        True if the soft threshold has been hit.

        :return: The soft_exceeded of this QuotaQuotaThresholdsExtended.
        :rtype: bool
        """
        return self._soft_exceeded

    @soft_exceeded.setter
    def soft_exceeded(self, soft_exceeded):
        """
        Sets the soft_exceeded of this QuotaQuotaThresholdsExtended.
        True if the soft threshold has been hit.

        :param soft_exceeded: The soft_exceeded of this QuotaQuotaThresholdsExtended.
        :type: bool
        """
        
        self._soft_exceeded = soft_exceeded

    @property
    def soft_last_exceeded(self):
        """
        Gets the soft_last_exceeded of this QuotaQuotaThresholdsExtended.
        Time at which soft threshold was hit

        :return: The soft_last_exceeded of this QuotaQuotaThresholdsExtended.
        :rtype: int
        """
        return self._soft_last_exceeded

    @soft_last_exceeded.setter
    def soft_last_exceeded(self, soft_last_exceeded):
        """
        Sets the soft_last_exceeded of this QuotaQuotaThresholdsExtended.
        Time at which soft threshold was hit

        :param soft_last_exceeded: The soft_last_exceeded of this QuotaQuotaThresholdsExtended.
        :type: int
        """
        
        self._soft_last_exceeded = soft_last_exceeded

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

