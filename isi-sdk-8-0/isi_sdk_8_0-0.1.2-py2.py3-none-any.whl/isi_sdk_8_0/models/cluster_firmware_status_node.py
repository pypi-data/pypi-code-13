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


class ClusterFirmwareStatusNode(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ClusterFirmwareStatusNode - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'devices': 'list[ClusterFirmwareStatusNodeDevice]',
            'lnn': 'int',
            'package': 'list[ClusterFirmwareStatusNodePackageItem]'
        }

        self.attribute_map = {
            'devices': 'devices',
            'lnn': 'lnn',
            'package': 'package'
        }

        self._devices = None
        self._lnn = None
        self._package = None

    @property
    def devices(self):
        """
        Gets the devices of this ClusterFirmwareStatusNode.
        List of the firmware status for hardware components on the node.

        :return: The devices of this ClusterFirmwareStatusNode.
        :rtype: list[ClusterFirmwareStatusNodeDevice]
        """
        return self._devices

    @devices.setter
    def devices(self, devices):
        """
        Sets the devices of this ClusterFirmwareStatusNode.
        List of the firmware status for hardware components on the node.

        :param devices: The devices of this ClusterFirmwareStatusNode.
        :type: list[ClusterFirmwareStatusNodeDevice]
        """
        
        self._devices = devices

    @property
    def lnn(self):
        """
        Gets the lnn of this ClusterFirmwareStatusNode.
        The lnn of the node.

        :return: The lnn of this ClusterFirmwareStatusNode.
        :rtype: int
        """
        return self._lnn

    @lnn.setter
    def lnn(self, lnn):
        """
        Sets the lnn of this ClusterFirmwareStatusNode.
        The lnn of the node.

        :param lnn: The lnn of this ClusterFirmwareStatusNode.
        :type: int
        """
        
        self._lnn = lnn

    @property
    def package(self):
        """
        Gets the package of this ClusterFirmwareStatusNode.
        List of the firmware binary information for the installed firmware package.

        :return: The package of this ClusterFirmwareStatusNode.
        :rtype: list[ClusterFirmwareStatusNodePackageItem]
        """
        return self._package

    @package.setter
    def package(self, package):
        """
        Sets the package of this ClusterFirmwareStatusNode.
        List of the firmware binary information for the installed firmware package.

        :param package: The package of this ClusterFirmwareStatusNode.
        :type: list[ClusterFirmwareStatusNodePackageItem]
        """
        
        self._package = package

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

