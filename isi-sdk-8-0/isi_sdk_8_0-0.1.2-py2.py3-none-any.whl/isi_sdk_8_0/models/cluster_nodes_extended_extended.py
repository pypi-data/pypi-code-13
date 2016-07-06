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


class ClusterNodesExtendedExtended(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ClusterNodesExtendedExtended - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'error': 'ClusterNodesError',
            'last_action': 'str',
            'last_action_result': 'str',
            'lnn': 'int',
            'node_state': 'str',
            'onefs_version': 'ClusterNodesOnefsVersion',
            'progress': 'int'
        }

        self.attribute_map = {
            'error': 'error',
            'last_action': 'last_action',
            'last_action_result': 'last_action_result',
            'lnn': 'lnn',
            'node_state': 'node_state',
            'onefs_version': 'onefs_version',
            'progress': 'progress'
        }

        self._error = None
        self._last_action = None
        self._last_action_result = None
        self._lnn = None
        self._node_state = None
        self._onefs_version = None
        self._progress = None

    @property
    def error(self):
        """
        Gets the error of this ClusterNodesExtendedExtended.
        The current OneFS version before upgrade.

        :return: The error of this ClusterNodesExtendedExtended.
        :rtype: ClusterNodesError
        """
        return self._error

    @error.setter
    def error(self, error):
        """
        Sets the error of this ClusterNodesExtendedExtended.
        The current OneFS version before upgrade.

        :param error: The error of this ClusterNodesExtendedExtended.
        :type: ClusterNodesError
        """
        
        self._error = error

    @property
    def last_action(self):
        """
        Gets the last_action of this ClusterNodesExtendedExtended.
        The last action performed to completion/failure on this node.  Null if the node_state is 'committed' or 'assessing.' One of the following values: 'upgrade', 'rollback'.

        :return: The last_action of this ClusterNodesExtendedExtended.
        :rtype: str
        """
        return self._last_action

    @last_action.setter
    def last_action(self, last_action):
        """
        Sets the last_action of this ClusterNodesExtendedExtended.
        The last action performed to completion/failure on this node.  Null if the node_state is 'committed' or 'assessing.' One of the following values: 'upgrade', 'rollback'.

        :param last_action: The last_action of this ClusterNodesExtendedExtended.
        :type: str
        """
        
        self._last_action = last_action

    @property
    def last_action_result(self):
        """
        Gets the last_action_result of this ClusterNodesExtendedExtended.
        Did the node pass upgrade or rollback without failing? Null if the node_state is 'committed.' One of the following values: 'pass', 'fail', null

        :return: The last_action_result of this ClusterNodesExtendedExtended.
        :rtype: str
        """
        return self._last_action_result

    @last_action_result.setter
    def last_action_result(self, last_action_result):
        """
        Sets the last_action_result of this ClusterNodesExtendedExtended.
        Did the node pass upgrade or rollback without failing? Null if the node_state is 'committed.' One of the following values: 'pass', 'fail', null

        :param last_action_result: The last_action_result of this ClusterNodesExtendedExtended.
        :type: str
        """
        
        self._last_action_result = last_action_result

    @property
    def lnn(self):
        """
        Gets the lnn of this ClusterNodesExtendedExtended.
        The lnn of the node.

        :return: The lnn of this ClusterNodesExtendedExtended.
        :rtype: int
        """
        return self._lnn

    @lnn.setter
    def lnn(self, lnn):
        """
        Sets the lnn of this ClusterNodesExtendedExtended.
        The lnn of the node.

        :param lnn: The lnn of this ClusterNodesExtendedExtended.
        :type: int
        """
        
        self._lnn = lnn

    @property
    def node_state(self):
        """
        Gets the node_state of this ClusterNodesExtendedExtended.
        The state of the node during the upgrade, rollback, or assessment. One of the following values: 'committed', 'upgraded', 'upgrading', 'rolling back', 'assessing', 'error'

        :return: The node_state of this ClusterNodesExtendedExtended.
        :rtype: str
        """
        return self._node_state

    @node_state.setter
    def node_state(self, node_state):
        """
        Sets the node_state of this ClusterNodesExtendedExtended.
        The state of the node during the upgrade, rollback, or assessment. One of the following values: 'committed', 'upgraded', 'upgrading', 'rolling back', 'assessing', 'error'

        :param node_state: The node_state of this ClusterNodesExtendedExtended.
        :type: str
        """
        
        self._node_state = node_state

    @property
    def onefs_version(self):
        """
        Gets the onefs_version of this ClusterNodesExtendedExtended.
        The current OneFS version before upgrade.

        :return: The onefs_version of this ClusterNodesExtendedExtended.
        :rtype: ClusterNodesOnefsVersion
        """
        return self._onefs_version

    @onefs_version.setter
    def onefs_version(self, onefs_version):
        """
        Sets the onefs_version of this ClusterNodesExtendedExtended.
        The current OneFS version before upgrade.

        :param onefs_version: The onefs_version of this ClusterNodesExtendedExtended.
        :type: ClusterNodesOnefsVersion
        """
        
        self._onefs_version = onefs_version

    @property
    def progress(self):
        """
        Gets the progress of this ClusterNodesExtendedExtended.
        What step is the upgrade, assessment, or rollback in? To show via progress indicator. NOTE: the value is an integer between 0 and 100 (percent)

        :return: The progress of this ClusterNodesExtendedExtended.
        :rtype: int
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """
        Sets the progress of this ClusterNodesExtendedExtended.
        What step is the upgrade, assessment, or rollback in? To show via progress indicator. NOTE: the value is an integer between 0 and 100 (percent)

        :param progress: The progress of this ClusterNodesExtendedExtended.
        :type: int
        """
        
        self._progress = progress

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

