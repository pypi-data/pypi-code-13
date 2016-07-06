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


class AuditSettingsSettings(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AuditSettingsSettings - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'audit_failure': 'list[str]',
            'audit_success': 'list[str]',
            'syslog_audit_events': 'list[str]',
            'syslog_forwarding_enabled': 'bool'
        }

        self.attribute_map = {
            'audit_failure': 'audit_failure',
            'audit_success': 'audit_success',
            'syslog_audit_events': 'syslog_audit_events',
            'syslog_forwarding_enabled': 'syslog_forwarding_enabled'
        }

        self._audit_failure = None
        self._audit_success = None
        self._syslog_audit_events = None
        self._syslog_forwarding_enabled = None

    @property
    def audit_failure(self):
        """
        Gets the audit_failure of this AuditSettingsSettings.
        Filter of protocol operations to Audit when they fail.

        :return: The audit_failure of this AuditSettingsSettings.
        :rtype: list[str]
        """
        return self._audit_failure

    @audit_failure.setter
    def audit_failure(self, audit_failure):
        """
        Sets the audit_failure of this AuditSettingsSettings.
        Filter of protocol operations to Audit when they fail.

        :param audit_failure: The audit_failure of this AuditSettingsSettings.
        :type: list[str]
        """
        
        self._audit_failure = audit_failure

    @property
    def audit_success(self):
        """
        Gets the audit_success of this AuditSettingsSettings.
        Filter of protocol operations to Audit when they succeed.

        :return: The audit_success of this AuditSettingsSettings.
        :rtype: list[str]
        """
        return self._audit_success

    @audit_success.setter
    def audit_success(self, audit_success):
        """
        Sets the audit_success of this AuditSettingsSettings.
        Filter of protocol operations to Audit when they succeed.

        :param audit_success: The audit_success of this AuditSettingsSettings.
        :type: list[str]
        """
        
        self._audit_success = audit_success

    @property
    def syslog_audit_events(self):
        """
        Gets the syslog_audit_events of this AuditSettingsSettings.
        Filter of Audit operations to forward to syslog.

        :return: The syslog_audit_events of this AuditSettingsSettings.
        :rtype: list[str]
        """
        return self._syslog_audit_events

    @syslog_audit_events.setter
    def syslog_audit_events(self, syslog_audit_events):
        """
        Sets the syslog_audit_events of this AuditSettingsSettings.
        Filter of Audit operations to forward to syslog.

        :param syslog_audit_events: The syslog_audit_events of this AuditSettingsSettings.
        :type: list[str]
        """
        
        self._syslog_audit_events = syslog_audit_events

    @property
    def syslog_forwarding_enabled(self):
        """
        Gets the syslog_forwarding_enabled of this AuditSettingsSettings.
        Enables forwarding of events to syslog.

        :return: The syslog_forwarding_enabled of this AuditSettingsSettings.
        :rtype: bool
        """
        return self._syslog_forwarding_enabled

    @syslog_forwarding_enabled.setter
    def syslog_forwarding_enabled(self, syslog_forwarding_enabled):
        """
        Sets the syslog_forwarding_enabled of this AuditSettingsSettings.
        Enables forwarding of events to syslog.

        :param syslog_forwarding_enabled: The syslog_forwarding_enabled of this AuditSettingsSettings.
        :type: bool
        """
        
        self._syslog_forwarding_enabled = syslog_forwarding_enabled

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

