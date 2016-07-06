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


class ClusterFirmwareUpgradeItem(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ClusterFirmwareUpgradeItem - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'exclude_device': 'str',
            'exclude_type': 'str',
            'include_device': 'str',
            'include_type': 'str',
            'no_burn': 'bool',
            'no_reboot': 'bool',
            'no_verify': 'bool',
            'nodes_to_upgrade': 'list[int]'
        }

        self.attribute_map = {
            'exclude_device': 'exclude_device',
            'exclude_type': 'exclude_type',
            'include_device': 'include_device',
            'include_type': 'include_type',
            'no_burn': 'no_burn',
            'no_reboot': 'no_reboot',
            'no_verify': 'no_verify',
            'nodes_to_upgrade': 'nodes_to_upgrade'
        }

        self._exclude_device = None
        self._exclude_type = None
        self._include_device = None
        self._include_type = None
        self._no_burn = None
        self._no_reboot = None
        self._no_verify = None
        self._nodes_to_upgrade = None

    @property
    def exclude_device(self):
        """
        Gets the exclude_device of this ClusterFirmwareUpgradeItem.
        Exclude the specified devices in the firmware upgrade.

        :return: The exclude_device of this ClusterFirmwareUpgradeItem.
        :rtype: str
        """
        return self._exclude_device

    @exclude_device.setter
    def exclude_device(self, exclude_device):
        """
        Sets the exclude_device of this ClusterFirmwareUpgradeItem.
        Exclude the specified devices in the firmware upgrade.

        :param exclude_device: The exclude_device of this ClusterFirmwareUpgradeItem.
        :type: str
        """
        
        self._exclude_device = exclude_device

    @property
    def exclude_type(self):
        """
        Gets the exclude_type of this ClusterFirmwareUpgradeItem.
        Include the specified device type in the firmware upgrade.

        :return: The exclude_type of this ClusterFirmwareUpgradeItem.
        :rtype: str
        """
        return self._exclude_type

    @exclude_type.setter
    def exclude_type(self, exclude_type):
        """
        Sets the exclude_type of this ClusterFirmwareUpgradeItem.
        Include the specified device type in the firmware upgrade.

        :param exclude_type: The exclude_type of this ClusterFirmwareUpgradeItem.
        :type: str
        """
        
        self._exclude_type = exclude_type

    @property
    def include_device(self):
        """
        Gets the include_device of this ClusterFirmwareUpgradeItem.
        Include the specified devices in the firmware upgrade.

        :return: The include_device of this ClusterFirmwareUpgradeItem.
        :rtype: str
        """
        return self._include_device

    @include_device.setter
    def include_device(self, include_device):
        """
        Sets the include_device of this ClusterFirmwareUpgradeItem.
        Include the specified devices in the firmware upgrade.

        :param include_device: The include_device of this ClusterFirmwareUpgradeItem.
        :type: str
        """
        
        self._include_device = include_device

    @property
    def include_type(self):
        """
        Gets the include_type of this ClusterFirmwareUpgradeItem.
        Include the specified device type in the firmware upgrade.

        :return: The include_type of this ClusterFirmwareUpgradeItem.
        :rtype: str
        """
        return self._include_type

    @include_type.setter
    def include_type(self, include_type):
        """
        Sets the include_type of this ClusterFirmwareUpgradeItem.
        Include the specified device type in the firmware upgrade.

        :param include_type: The include_type of this ClusterFirmwareUpgradeItem.
        :type: str
        """
        
        self._include_type = include_type

    @property
    def no_burn(self):
        """
        Gets the no_burn of this ClusterFirmwareUpgradeItem.
        Do not burn the firmware.

        :return: The no_burn of this ClusterFirmwareUpgradeItem.
        :rtype: bool
        """
        return self._no_burn

    @no_burn.setter
    def no_burn(self, no_burn):
        """
        Sets the no_burn of this ClusterFirmwareUpgradeItem.
        Do not burn the firmware.

        :param no_burn: The no_burn of this ClusterFirmwareUpgradeItem.
        :type: bool
        """
        
        self._no_burn = no_burn

    @property
    def no_reboot(self):
        """
        Gets the no_reboot of this ClusterFirmwareUpgradeItem.
        Do not reboot the node after an upgrade

        :return: The no_reboot of this ClusterFirmwareUpgradeItem.
        :rtype: bool
        """
        return self._no_reboot

    @no_reboot.setter
    def no_reboot(self, no_reboot):
        """
        Sets the no_reboot of this ClusterFirmwareUpgradeItem.
        Do not reboot the node after an upgrade

        :param no_reboot: The no_reboot of this ClusterFirmwareUpgradeItem.
        :type: bool
        """
        
        self._no_reboot = no_reboot

    @property
    def no_verify(self):
        """
        Gets the no_verify of this ClusterFirmwareUpgradeItem.
        Do not verify the firmware upgrade after an upgrade.

        :return: The no_verify of this ClusterFirmwareUpgradeItem.
        :rtype: bool
        """
        return self._no_verify

    @no_verify.setter
    def no_verify(self, no_verify):
        """
        Sets the no_verify of this ClusterFirmwareUpgradeItem.
        Do not verify the firmware upgrade after an upgrade.

        :param no_verify: The no_verify of this ClusterFirmwareUpgradeItem.
        :type: bool
        """
        
        self._no_verify = no_verify

    @property
    def nodes_to_upgrade(self):
        """
        Gets the nodes_to_upgrade of this ClusterFirmwareUpgradeItem.
        The nodes scheduled for upgrade. Order in array determines queue position number. 'All' and null option will upgrade all nodes in <lnn> order.

        :return: The nodes_to_upgrade of this ClusterFirmwareUpgradeItem.
        :rtype: list[int]
        """
        return self._nodes_to_upgrade

    @nodes_to_upgrade.setter
    def nodes_to_upgrade(self, nodes_to_upgrade):
        """
        Sets the nodes_to_upgrade of this ClusterFirmwareUpgradeItem.
        The nodes scheduled for upgrade. Order in array determines queue position number. 'All' and null option will upgrade all nodes in <lnn> order.

        :param nodes_to_upgrade: The nodes_to_upgrade of this ClusterFirmwareUpgradeItem.
        :type: list[int]
        """
        
        self._nodes_to_upgrade = nodes_to_upgrade

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

