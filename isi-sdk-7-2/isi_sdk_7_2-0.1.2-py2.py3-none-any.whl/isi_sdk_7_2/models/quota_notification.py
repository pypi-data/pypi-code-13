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


class QuotaNotification(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        QuotaNotification - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'action_alert': 'bool',
            'action_email_address': 'str',
            'action_email_owner': 'bool',
            'email_template': 'str',
            'holdoff': 'int',
            'schedule': 'str'
        }

        self.attribute_map = {
            'action_alert': 'action_alert',
            'action_email_address': 'action_email_address',
            'action_email_owner': 'action_email_owner',
            'email_template': 'email_template',
            'holdoff': 'holdoff',
            'schedule': 'schedule'
        }

        self._action_alert = None
        self._action_email_address = None
        self._action_email_owner = None
        self._email_template = None
        self._holdoff = None
        self._schedule = None

    @property
    def action_alert(self):
        """
        Gets the action_alert of this QuotaNotification.
        Send alert when rule matches.

        :return: The action_alert of this QuotaNotification.
        :rtype: bool
        """
        return self._action_alert

    @action_alert.setter
    def action_alert(self, action_alert):
        """
        Sets the action_alert of this QuotaNotification.
        Send alert when rule matches.

        :param action_alert: The action_alert of this QuotaNotification.
        :type: bool
        """
        
        self._action_alert = action_alert

    @property
    def action_email_address(self):
        """
        Gets the action_email_address of this QuotaNotification.
        Email a specific email address when rule matches.

        :return: The action_email_address of this QuotaNotification.
        :rtype: str
        """
        return self._action_email_address

    @action_email_address.setter
    def action_email_address(self, action_email_address):
        """
        Sets the action_email_address of this QuotaNotification.
        Email a specific email address when rule matches.

        :param action_email_address: The action_email_address of this QuotaNotification.
        :type: str
        """
        
        self._action_email_address = action_email_address

    @property
    def action_email_owner(self):
        """
        Gets the action_email_owner of this QuotaNotification.
        Email quota domain owner when rule matches.

        :return: The action_email_owner of this QuotaNotification.
        :rtype: bool
        """
        return self._action_email_owner

    @action_email_owner.setter
    def action_email_owner(self, action_email_owner):
        """
        Sets the action_email_owner of this QuotaNotification.
        Email quota domain owner when rule matches.

        :param action_email_owner: The action_email_owner of this QuotaNotification.
        :type: bool
        """
        
        self._action_email_owner = action_email_owner

    @property
    def email_template(self):
        """
        Gets the email_template of this QuotaNotification.
        Path of optional /ifs template file used for email actions.

        :return: The email_template of this QuotaNotification.
        :rtype: str
        """
        return self._email_template

    @email_template.setter
    def email_template(self, email_template):
        """
        Sets the email_template of this QuotaNotification.
        Path of optional /ifs template file used for email actions.

        :param email_template: The email_template of this QuotaNotification.
        :type: str
        """
        
        self._email_template = email_template

    @property
    def holdoff(self):
        """
        Gets the holdoff of this QuotaNotification.
        Time to wait between detections for rules triggered by user actions.

        :return: The holdoff of this QuotaNotification.
        :rtype: int
        """
        return self._holdoff

    @holdoff.setter
    def holdoff(self, holdoff):
        """
        Sets the holdoff of this QuotaNotification.
        Time to wait between detections for rules triggered by user actions.

        :param holdoff: The holdoff of this QuotaNotification.
        :type: int
        """
        
        self._holdoff = holdoff

    @property
    def schedule(self):
        """
        Gets the schedule of this QuotaNotification.
        Schedule for rules that repeatedly notify.

        :return: The schedule of this QuotaNotification.
        :rtype: str
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """
        Sets the schedule of this QuotaNotification.
        Schedule for rules that repeatedly notify.

        :param schedule: The schedule of this QuotaNotification.
        :type: str
        """
        
        self._schedule = schedule

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

