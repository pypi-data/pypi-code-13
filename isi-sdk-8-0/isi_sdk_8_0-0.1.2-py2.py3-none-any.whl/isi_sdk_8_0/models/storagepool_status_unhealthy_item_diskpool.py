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


class StoragepoolStatusUnhealthyItemDiskpool(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        StoragepoolStatusUnhealthyItemDiskpool - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'drives': 'list[StoragepoolStatusUnprovisionedItem]',
            'id': 'int',
            'name': 'str',
            'nodepool_id': 'int',
            'protection_policy': 'str',
            'ssd_drives': 'list[StoragepoolStatusUnprovisionedItem]'
        }

        self.attribute_map = {
            'drives': 'drives',
            'id': 'id',
            'name': 'name',
            'nodepool_id': 'nodepool_id',
            'protection_policy': 'protection_policy',
            'ssd_drives': 'ssd_drives'
        }

        self._drives = None
        self._id = None
        self._name = None
        self._nodepool_id = None
        self._protection_policy = None
        self._ssd_drives = None

    @property
    def drives(self):
        """
        Gets the drives of this StoragepoolStatusUnhealthyItemDiskpool.
        The drives that are part of this disk pool.

        :return: The drives of this StoragepoolStatusUnhealthyItemDiskpool.
        :rtype: list[StoragepoolStatusUnprovisionedItem]
        """
        return self._drives

    @drives.setter
    def drives(self, drives):
        """
        Sets the drives of this StoragepoolStatusUnhealthyItemDiskpool.
        The drives that are part of this disk pool.

        :param drives: The drives of this StoragepoolStatusUnhealthyItemDiskpool.
        :type: list[StoragepoolStatusUnprovisionedItem]
        """
        
        self._drives = drives

    @property
    def id(self):
        """
        Gets the id of this StoragepoolStatusUnhealthyItemDiskpool.
        The system ID given to the disk pool.

        :return: The id of this StoragepoolStatusUnhealthyItemDiskpool.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this StoragepoolStatusUnhealthyItemDiskpool.
        The system ID given to the disk pool.

        :param id: The id of this StoragepoolStatusUnhealthyItemDiskpool.
        :type: int
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this StoragepoolStatusUnhealthyItemDiskpool.
        The disk pool name.

        :return: The name of this StoragepoolStatusUnhealthyItemDiskpool.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this StoragepoolStatusUnhealthyItemDiskpool.
        The disk pool name.

        :param name: The name of this StoragepoolStatusUnhealthyItemDiskpool.
        :type: str
        """
        
        self._name = name

    @property
    def nodepool_id(self):
        """
        Gets the nodepool_id of this StoragepoolStatusUnhealthyItemDiskpool.
        The system ID of the disk pool's node pool, if it is in a node pool.

        :return: The nodepool_id of this StoragepoolStatusUnhealthyItemDiskpool.
        :rtype: int
        """
        return self._nodepool_id

    @nodepool_id.setter
    def nodepool_id(self, nodepool_id):
        """
        Sets the nodepool_id of this StoragepoolStatusUnhealthyItemDiskpool.
        The system ID of the disk pool's node pool, if it is in a node pool.

        :param nodepool_id: The nodepool_id of this StoragepoolStatusUnhealthyItemDiskpool.
        :type: int
        """
        
        self._nodepool_id = nodepool_id

    @property
    def protection_policy(self):
        """
        Gets the protection_policy of this StoragepoolStatusUnhealthyItemDiskpool.
        The protection policy for the disk pool.

        :return: The protection_policy of this StoragepoolStatusUnhealthyItemDiskpool.
        :rtype: str
        """
        return self._protection_policy

    @protection_policy.setter
    def protection_policy(self, protection_policy):
        """
        Sets the protection_policy of this StoragepoolStatusUnhealthyItemDiskpool.
        The protection policy for the disk pool.

        :param protection_policy: The protection_policy of this StoragepoolStatusUnhealthyItemDiskpool.
        :type: str
        """
        
        self._protection_policy = protection_policy

    @property
    def ssd_drives(self):
        """
        Gets the ssd_drives of this StoragepoolStatusUnhealthyItemDiskpool.
        The SSDs that are part of this disk pool.

        :return: The ssd_drives of this StoragepoolStatusUnhealthyItemDiskpool.
        :rtype: list[StoragepoolStatusUnprovisionedItem]
        """
        return self._ssd_drives

    @ssd_drives.setter
    def ssd_drives(self, ssd_drives):
        """
        Sets the ssd_drives of this StoragepoolStatusUnhealthyItemDiskpool.
        The SSDs that are part of this disk pool.

        :param ssd_drives: The ssd_drives of this StoragepoolStatusUnhealthyItemDiskpool.
        :type: list[StoragepoolStatusUnprovisionedItem]
        """
        
        self._ssd_drives = ssd_drives

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

