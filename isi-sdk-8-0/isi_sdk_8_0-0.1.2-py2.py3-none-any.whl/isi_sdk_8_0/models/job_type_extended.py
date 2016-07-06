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


class JobTypeExtended(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        JobTypeExtended - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'enabled': 'bool',
            'policy': 'str',
            'priority': 'int',
            'schedule': 'str',
            'allow_multiple_instances': 'bool',
            'description': 'str',
            'exclusion_set': 'str',
            'hidden': 'bool',
            'id': 'str'
        }

        self.attribute_map = {
            'enabled': 'enabled',
            'policy': 'policy',
            'priority': 'priority',
            'schedule': 'schedule',
            'allow_multiple_instances': 'allow_multiple_instances',
            'description': 'description',
            'exclusion_set': 'exclusion_set',
            'hidden': 'hidden',
            'id': 'id'
        }

        self._enabled = None
        self._policy = None
        self._priority = None
        self._schedule = None
        self._allow_multiple_instances = None
        self._description = None
        self._exclusion_set = None
        self._hidden = None
        self._id = None

    @property
    def enabled(self):
        """
        Gets the enabled of this JobTypeExtended.
        Whether the job type is enabled and able to run.

        :return: The enabled of this JobTypeExtended.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this JobTypeExtended.
        Whether the job type is enabled and able to run.

        :param enabled: The enabled of this JobTypeExtended.
        :type: bool
        """
        
        self._enabled = enabled

    @property
    def policy(self):
        """
        Gets the policy of this JobTypeExtended.
        Default impact policy of this job type.

        :return: The policy of this JobTypeExtended.
        :rtype: str
        """
        return self._policy

    @policy.setter
    def policy(self, policy):
        """
        Sets the policy of this JobTypeExtended.
        Default impact policy of this job type.

        :param policy: The policy of this JobTypeExtended.
        :type: str
        """
        
        self._policy = policy

    @property
    def priority(self):
        """
        Gets the priority of this JobTypeExtended.
        Default priority of this job type; lower numbers preempt higher numbers.

        :return: The priority of this JobTypeExtended.
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """
        Sets the priority of this JobTypeExtended.
        Default priority of this job type; lower numbers preempt higher numbers.

        :param priority: The priority of this JobTypeExtended.
        :type: int
        """
        
        if priority is not None  and priority > 10.0:
            raise ValueError("Invalid value for `priority`, must be a value less than or equal to `10.0`")
        if priority is not None and priority < 1.0:
            raise ValueError("Invalid value for `priority`, must be a value greater than or equal to `1.0`")

        self._priority = priority

    @property
    def schedule(self):
        """
        Gets the schedule of this JobTypeExtended.
        The schedule on which this job type is queued, if any.

        :return: The schedule of this JobTypeExtended.
        :rtype: str
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """
        Sets the schedule of this JobTypeExtended.
        The schedule on which this job type is queued, if any.

        :param schedule: The schedule of this JobTypeExtended.
        :type: str
        """
        
        self._schedule = schedule

    @property
    def allow_multiple_instances(self):
        """
        Gets the allow_multiple_instances of this JobTypeExtended.
        Whether multiple instances of this job type may run simultaneously.

        :return: The allow_multiple_instances of this JobTypeExtended.
        :rtype: bool
        """
        return self._allow_multiple_instances

    @allow_multiple_instances.setter
    def allow_multiple_instances(self, allow_multiple_instances):
        """
        Sets the allow_multiple_instances of this JobTypeExtended.
        Whether multiple instances of this job type may run simultaneously.

        :param allow_multiple_instances: The allow_multiple_instances of this JobTypeExtended.
        :type: bool
        """
        
        self._allow_multiple_instances = allow_multiple_instances

    @property
    def description(self):
        """
        Gets the description of this JobTypeExtended.
        Brief description of the job type.

        :return: The description of this JobTypeExtended.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this JobTypeExtended.
        Brief description of the job type.

        :param description: The description of this JobTypeExtended.
        :type: str
        """
        
        self._description = description

    @property
    def exclusion_set(self):
        """
        Gets the exclusion_set of this JobTypeExtended.
        The set(s) of mutually-exclusive job types to which this job belongs.  No job in this set may run with any other job in this set.  Obsolete; this value will always be an empty string, as exclusion sets are no longer a job type property.

        :return: The exclusion_set of this JobTypeExtended.
        :rtype: str
        """
        return self._exclusion_set

    @exclusion_set.setter
    def exclusion_set(self, exclusion_set):
        """
        Sets the exclusion_set of this JobTypeExtended.
        The set(s) of mutually-exclusive job types to which this job belongs.  No job in this set may run with any other job in this set.  Obsolete; this value will always be an empty string, as exclusion sets are no longer a job type property.

        :param exclusion_set: The exclusion_set of this JobTypeExtended.
        :type: str
        """
        
        self._exclusion_set = exclusion_set

    @property
    def hidden(self):
        """
        Gets the hidden of this JobTypeExtended.
        Whether this job type is normally visible in the UI.

        :return: The hidden of this JobTypeExtended.
        :rtype: bool
        """
        return self._hidden

    @hidden.setter
    def hidden(self, hidden):
        """
        Sets the hidden of this JobTypeExtended.
        Whether this job type is normally visible in the UI.

        :param hidden: The hidden of this JobTypeExtended.
        :type: bool
        """
        
        self._hidden = hidden

    @property
    def id(self):
        """
        Gets the id of this JobTypeExtended.
        Job type ID.

        :return: The id of this JobTypeExtended.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this JobTypeExtended.
        Job type ID.

        :param id: The id of this JobTypeExtended.
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

