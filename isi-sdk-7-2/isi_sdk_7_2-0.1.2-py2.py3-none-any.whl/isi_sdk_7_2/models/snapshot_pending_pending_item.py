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


class SnapshotPendingPendingItem(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        SnapshotPendingPendingItem - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'path': 'str',
            'schedule': 'str',
            'snapshot': 'str',
            'time': 'int'
        }

        self.attribute_map = {
            'id': 'id',
            'path': 'path',
            'schedule': 'schedule',
            'snapshot': 'snapshot',
            'time': 'time'
        }

        self._id = None
        self._path = None
        self._schedule = None
        self._snapshot = None
        self._time = None

    @property
    def id(self):
        """
        Gets the id of this SnapshotPendingPendingItem.
        The system supplied unique ID used for sorting and paging.

        :return: The id of this SnapshotPendingPendingItem.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this SnapshotPendingPendingItem.
        The system supplied unique ID used for sorting and paging.

        :param id: The id of this SnapshotPendingPendingItem.
        :type: str
        """
        
        self._id = id

    @property
    def path(self):
        """
        Gets the path of this SnapshotPendingPendingItem.
        The /ifs path that will snapshotted.

        :return: The path of this SnapshotPendingPendingItem.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """
        Sets the path of this SnapshotPendingPendingItem.
        The /ifs path that will snapshotted.

        :param path: The path of this SnapshotPendingPendingItem.
        :type: str
        """
        
        self._path = path

    @property
    def schedule(self):
        """
        Gets the schedule of this SnapshotPendingPendingItem.
        The name of the schedule used to create this snapshot.

        :return: The schedule of this SnapshotPendingPendingItem.
        :rtype: str
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """
        Sets the schedule of this SnapshotPendingPendingItem.
        The name of the schedule used to create this snapshot.

        :param schedule: The schedule of this SnapshotPendingPendingItem.
        :type: str
        """
        
        self._schedule = schedule

    @property
    def snapshot(self):
        """
        Gets the snapshot of this SnapshotPendingPendingItem.
        The system snapshot name formed from the schedule formate.

        :return: The snapshot of this SnapshotPendingPendingItem.
        :rtype: str
        """
        return self._snapshot

    @snapshot.setter
    def snapshot(self, snapshot):
        """
        Sets the snapshot of this SnapshotPendingPendingItem.
        The system snapshot name formed from the schedule formate.

        :param snapshot: The snapshot of this SnapshotPendingPendingItem.
        :type: str
        """
        
        self._snapshot = snapshot

    @property
    def time(self):
        """
        Gets the time of this SnapshotPendingPendingItem.
        The Unix Epoch time the snapshot will be created.

        :return: The time of this SnapshotPendingPendingItem.
        :rtype: int
        """
        return self._time

    @time.setter
    def time(self, time):
        """
        Sets the time of this SnapshotPendingPendingItem.
        The Unix Epoch time the snapshot will be created.

        :param time: The time of this SnapshotPendingPendingItem.
        :type: int
        """
        
        self._time = time

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

