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


class FilepoolPolicyExtendedExtended(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        FilepoolPolicyExtendedExtended - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'actions': 'list[FilepoolPolicyActionExtended]',
            'apply_order': 'int',
            'birth_cluster_id': 'str',
            'description': 'str',
            'file_matching_pattern': 'FilepoolPolicyFileMatchingPattern',
            'id': 'int',
            'name': 'str',
            'state': 'str',
            'state_details': 'str'
        }

        self.attribute_map = {
            'actions': 'actions',
            'apply_order': 'apply_order',
            'birth_cluster_id': 'birth_cluster_id',
            'description': 'description',
            'file_matching_pattern': 'file_matching_pattern',
            'id': 'id',
            'name': 'name',
            'state': 'state',
            'state_details': 'state_details'
        }

        self._actions = None
        self._apply_order = None
        self._birth_cluster_id = None
        self._description = None
        self._file_matching_pattern = None
        self._id = None
        self._name = None
        self._state = None
        self._state_details = None

    @property
    def actions(self):
        """
        Gets the actions of this FilepoolPolicyExtendedExtended.
        A list of actions to be taken for matching files

        :return: The actions of this FilepoolPolicyExtendedExtended.
        :rtype: list[FilepoolPolicyActionExtended]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """
        Sets the actions of this FilepoolPolicyExtendedExtended.
        A list of actions to be taken for matching files

        :param actions: The actions of this FilepoolPolicyExtendedExtended.
        :type: list[FilepoolPolicyActionExtended]
        """
        
        self._actions = actions

    @property
    def apply_order(self):
        """
        Gets the apply_order of this FilepoolPolicyExtendedExtended.
        The order in which this policy should be applied (relative to other policies)

        :return: The apply_order of this FilepoolPolicyExtendedExtended.
        :rtype: int
        """
        return self._apply_order

    @apply_order.setter
    def apply_order(self, apply_order):
        """
        Sets the apply_order of this FilepoolPolicyExtendedExtended.
        The order in which this policy should be applied (relative to other policies)

        :param apply_order: The apply_order of this FilepoolPolicyExtendedExtended.
        :type: int
        """
        
        self._apply_order = apply_order

    @property
    def birth_cluster_id(self):
        """
        Gets the birth_cluster_id of this FilepoolPolicyExtendedExtended.
        The guid assigned to the cluster on which the account was created

        :return: The birth_cluster_id of this FilepoolPolicyExtendedExtended.
        :rtype: str
        """
        return self._birth_cluster_id

    @birth_cluster_id.setter
    def birth_cluster_id(self, birth_cluster_id):
        """
        Sets the birth_cluster_id of this FilepoolPolicyExtendedExtended.
        The guid assigned to the cluster on which the account was created

        :param birth_cluster_id: The birth_cluster_id of this FilepoolPolicyExtendedExtended.
        :type: str
        """
        
        self._birth_cluster_id = birth_cluster_id

    @property
    def description(self):
        """
        Gets the description of this FilepoolPolicyExtendedExtended.
        A description for this policy

        :return: The description of this FilepoolPolicyExtendedExtended.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this FilepoolPolicyExtendedExtended.
        A description for this policy

        :param description: The description of this FilepoolPolicyExtendedExtended.
        :type: str
        """
        
        self._description = description

    @property
    def file_matching_pattern(self):
        """
        Gets the file_matching_pattern of this FilepoolPolicyExtendedExtended.
        The file matching rules for this policy

        :return: The file_matching_pattern of this FilepoolPolicyExtendedExtended.
        :rtype: FilepoolPolicyFileMatchingPattern
        """
        return self._file_matching_pattern

    @file_matching_pattern.setter
    def file_matching_pattern(self, file_matching_pattern):
        """
        Sets the file_matching_pattern of this FilepoolPolicyExtendedExtended.
        The file matching rules for this policy

        :param file_matching_pattern: The file_matching_pattern of this FilepoolPolicyExtendedExtended.
        :type: FilepoolPolicyFileMatchingPattern
        """
        
        self._file_matching_pattern = file_matching_pattern

    @property
    def id(self):
        """
        Gets the id of this FilepoolPolicyExtendedExtended.
        A unique identifier for this policy

        :return: The id of this FilepoolPolicyExtendedExtended.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this FilepoolPolicyExtendedExtended.
        A unique identifier for this policy

        :param id: The id of this FilepoolPolicyExtendedExtended.
        :type: int
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this FilepoolPolicyExtendedExtended.
        A unique name for this policy

        :return: The name of this FilepoolPolicyExtendedExtended.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this FilepoolPolicyExtendedExtended.
        A unique name for this policy

        :param name: The name of this FilepoolPolicyExtendedExtended.
        :type: str
        """
        
        self._name = name

    @property
    def state(self):
        """
        Gets the state of this FilepoolPolicyExtendedExtended.
        Indicates whether this policy is in a good state (\"OK\") or disabled (\"disabled\")

        :return: The state of this FilepoolPolicyExtendedExtended.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this FilepoolPolicyExtendedExtended.
        Indicates whether this policy is in a good state (\"OK\") or disabled (\"disabled\")

        :param state: The state of this FilepoolPolicyExtendedExtended.
        :type: str
        """
        allowed_values = ["OK", "disabled"]
        if state is not None and state not in allowed_values:
            raise ValueError(
                "Invalid value for `state`, must be one of {0}"
                .format(allowed_values)
            )

        self._state = state

    @property
    def state_details(self):
        """
        Gets the state_details of this FilepoolPolicyExtendedExtended.
        Gives further information to describe the state of this policy

        :return: The state_details of this FilepoolPolicyExtendedExtended.
        :rtype: str
        """
        return self._state_details

    @state_details.setter
    def state_details(self, state_details):
        """
        Sets the state_details of this FilepoolPolicyExtendedExtended.
        Gives further information to describe the state of this policy

        :param state_details: The state_details of this FilepoolPolicyExtendedExtended.
        :type: str
        """
        
        self._state_details = state_details

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

