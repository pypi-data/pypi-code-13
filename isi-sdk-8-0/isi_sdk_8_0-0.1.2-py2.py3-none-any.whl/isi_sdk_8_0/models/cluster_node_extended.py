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


class ClusterNodeExtended(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ClusterNodeExtended - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'drives': 'list[NodeDrivesNodeDrive]',
            'hardware': 'ClusterNodeHardware',
            'id': 'int',
            'lnn': 'int',
            'partitions': 'ClusterNodePartitions',
            'sensors': 'ClusterNodeSensors',
            'state': 'ClusterNodeStateExtended',
            'status': 'ClusterNodeStatus'
        }

        self.attribute_map = {
            'drives': 'drives',
            'hardware': 'hardware',
            'id': 'id',
            'lnn': 'lnn',
            'partitions': 'partitions',
            'sensors': 'sensors',
            'state': 'state',
            'status': 'status'
        }

        self._drives = None
        self._hardware = None
        self._id = None
        self._lnn = None
        self._partitions = None
        self._sensors = None
        self._state = None
        self._status = None

    @property
    def drives(self):
        """
        Gets the drives of this ClusterNodeExtended.
        List of the drives in this node.

        :return: The drives of this ClusterNodeExtended.
        :rtype: list[NodeDrivesNodeDrive]
        """
        return self._drives

    @drives.setter
    def drives(self, drives):
        """
        Sets the drives of this ClusterNodeExtended.
        List of the drives in this node.

        :param drives: The drives of this ClusterNodeExtended.
        :type: list[NodeDrivesNodeDrive]
        """
        
        self._drives = drives

    @property
    def hardware(self):
        """
        Gets the hardware of this ClusterNodeExtended.
        Node hardware identifying information (static).

        :return: The hardware of this ClusterNodeExtended.
        :rtype: ClusterNodeHardware
        """
        return self._hardware

    @hardware.setter
    def hardware(self, hardware):
        """
        Sets the hardware of this ClusterNodeExtended.
        Node hardware identifying information (static).

        :param hardware: The hardware of this ClusterNodeExtended.
        :type: ClusterNodeHardware
        """
        
        self._hardware = hardware

    @property
    def id(self):
        """
        Gets the id of this ClusterNodeExtended.
        Node ID (Device Number) of this node.

        :return: The id of this ClusterNodeExtended.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ClusterNodeExtended.
        Node ID (Device Number) of this node.

        :param id: The id of this ClusterNodeExtended.
        :type: int
        """
        
        self._id = id

    @property
    def lnn(self):
        """
        Gets the lnn of this ClusterNodeExtended.
        Logical Node Number (LNN) of this node.

        :return: The lnn of this ClusterNodeExtended.
        :rtype: int
        """
        return self._lnn

    @lnn.setter
    def lnn(self, lnn):
        """
        Sets the lnn of this ClusterNodeExtended.
        Logical Node Number (LNN) of this node.

        :param lnn: The lnn of this ClusterNodeExtended.
        :type: int
        """
        
        self._lnn = lnn

    @property
    def partitions(self):
        """
        Gets the partitions of this ClusterNodeExtended.
        Node partition information.

        :return: The partitions of this ClusterNodeExtended.
        :rtype: ClusterNodePartitions
        """
        return self._partitions

    @partitions.setter
    def partitions(self, partitions):
        """
        Sets the partitions of this ClusterNodeExtended.
        Node partition information.

        :param partitions: The partitions of this ClusterNodeExtended.
        :type: ClusterNodePartitions
        """
        
        self._partitions = partitions

    @property
    def sensors(self):
        """
        Gets the sensors of this ClusterNodeExtended.
        Node sensor information (hardware reported).

        :return: The sensors of this ClusterNodeExtended.
        :rtype: ClusterNodeSensors
        """
        return self._sensors

    @sensors.setter
    def sensors(self, sensors):
        """
        Sets the sensors of this ClusterNodeExtended.
        Node sensor information (hardware reported).

        :param sensors: The sensors of this ClusterNodeExtended.
        :type: ClusterNodeSensors
        """
        
        self._sensors = sensors

    @property
    def state(self):
        """
        Gets the state of this ClusterNodeExtended.
        Node state information (reported and modifiable).

        :return: The state of this ClusterNodeExtended.
        :rtype: ClusterNodeStateExtended
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this ClusterNodeExtended.
        Node state information (reported and modifiable).

        :param state: The state of this ClusterNodeExtended.
        :type: ClusterNodeStateExtended
        """
        
        self._state = state

    @property
    def status(self):
        """
        Gets the status of this ClusterNodeExtended.
        Node status information (hardware reported).

        :return: The status of this ClusterNodeExtended.
        :rtype: ClusterNodeStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this ClusterNodeExtended.
        Node status information (hardware reported).

        :param status: The status of this ClusterNodeExtended.
        :type: ClusterNodeStatus
        """
        
        self._status = status

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

