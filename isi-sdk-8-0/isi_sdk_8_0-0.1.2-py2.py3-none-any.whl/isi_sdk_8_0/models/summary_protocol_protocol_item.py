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


class SummaryProtocolProtocolItem(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        SummaryProtocolProtocolItem - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            '_class': 'str',
            '_in': 'float',
            'in_avg': 'float',
            'in_max': 'float',
            'in_min': 'float',
            'in_standard_dev': 'float',
            'node': 'int',
            'operation': 'str',
            'operation_count': 'int',
            'operation_rate': 'float',
            'out': 'float',
            'out_avg': 'float',
            'out_max': 'float',
            'out_min': 'float',
            'out_standard_dev': 'float',
            'protocol': 'str',
            'time': 'int',
            'time_avg': 'float',
            'time_max': 'float',
            'time_min': 'float',
            'time_standard_dev': 'float'
        }

        self.attribute_map = {
            '_class': 'class',
            '_in': 'in',
            'in_avg': 'in_avg',
            'in_max': 'in_max',
            'in_min': 'in_min',
            'in_standard_dev': 'in_standard_dev',
            'node': 'node',
            'operation': 'operation',
            'operation_count': 'operation_count',
            'operation_rate': 'operation_rate',
            'out': 'out',
            'out_avg': 'out_avg',
            'out_max': 'out_max',
            'out_min': 'out_min',
            'out_standard_dev': 'out_standard_dev',
            'protocol': 'protocol',
            'time': 'time',
            'time_avg': 'time_avg',
            'time_max': 'time_max',
            'time_min': 'time_min',
            'time_standard_dev': 'time_standard_dev'
        }

        self.__class = None
        self.__in = None
        self._in_avg = None
        self._in_max = None
        self._in_min = None
        self._in_standard_dev = None
        self._node = None
        self._operation = None
        self._operation_count = None
        self._operation_rate = None
        self._out = None
        self._out_avg = None
        self._out_max = None
        self._out_min = None
        self._out_standard_dev = None
        self._protocol = None
        self._time = None
        self._time_avg = None
        self._time_max = None
        self._time_min = None
        self._time_standard_dev = None

    @property
    def _class(self):
        """
        Gets the _class of this SummaryProtocolProtocolItem.
        The class of the operation.

        :return: The _class of this SummaryProtocolProtocolItem.
        :rtype: str
        """
        return self.__class

    @_class.setter
    def _class(self, _class):
        """
        Sets the _class of this SummaryProtocolProtocolItem.
        The class of the operation.

        :param _class: The _class of this SummaryProtocolProtocolItem.
        :type: str
        """
        
        self.__class = _class

    @property
    def _in(self):
        """
        Gets the _in of this SummaryProtocolProtocolItem.
        Rate of input (in bytes/second) for an operation since the last time isi statistics collected the data.

        :return: The _in of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self.__in

    @_in.setter
    def _in(self, _in):
        """
        Sets the _in of this SummaryProtocolProtocolItem.
        Rate of input (in bytes/second) for an operation since the last time isi statistics collected the data.

        :param _in: The _in of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self.__in = _in

    @property
    def in_avg(self):
        """
        Gets the in_avg of this SummaryProtocolProtocolItem.
        Average input (received) bytes for an operation, in bytes.

        :return: The in_avg of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._in_avg

    @in_avg.setter
    def in_avg(self, in_avg):
        """
        Sets the in_avg of this SummaryProtocolProtocolItem.
        Average input (received) bytes for an operation, in bytes.

        :param in_avg: The in_avg of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._in_avg = in_avg

    @property
    def in_max(self):
        """
        Gets the in_max of this SummaryProtocolProtocolItem.
        Maximum input (received) bytes for an operation, in bytes.

        :return: The in_max of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._in_max

    @in_max.setter
    def in_max(self, in_max):
        """
        Sets the in_max of this SummaryProtocolProtocolItem.
        Maximum input (received) bytes for an operation, in bytes.

        :param in_max: The in_max of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._in_max = in_max

    @property
    def in_min(self):
        """
        Gets the in_min of this SummaryProtocolProtocolItem.
        Minimum input (received) bytes for an operation, in bytes.

        :return: The in_min of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._in_min

    @in_min.setter
    def in_min(self, in_min):
        """
        Sets the in_min of this SummaryProtocolProtocolItem.
        Minimum input (received) bytes for an operation, in bytes.

        :param in_min: The in_min of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._in_min = in_min

    @property
    def in_standard_dev(self):
        """
        Gets the in_standard_dev of this SummaryProtocolProtocolItem.
        Standard deviation for input (received) bytes for an operation, in bytes.

        :return: The in_standard_dev of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._in_standard_dev

    @in_standard_dev.setter
    def in_standard_dev(self, in_standard_dev):
        """
        Sets the in_standard_dev of this SummaryProtocolProtocolItem.
        Standard deviation for input (received) bytes for an operation, in bytes.

        :param in_standard_dev: The in_standard_dev of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._in_standard_dev = in_standard_dev

    @property
    def node(self):
        """
        Gets the node of this SummaryProtocolProtocolItem.
        The node on which the operation was performed.

        :return: The node of this SummaryProtocolProtocolItem.
        :rtype: int
        """
        return self._node

    @node.setter
    def node(self, node):
        """
        Sets the node of this SummaryProtocolProtocolItem.
        The node on which the operation was performed.

        :param node: The node of this SummaryProtocolProtocolItem.
        :type: int
        """
        
        self._node = node

    @property
    def operation(self):
        """
        Gets the operation of this SummaryProtocolProtocolItem.
        The operation performed.

        :return: The operation of this SummaryProtocolProtocolItem.
        :rtype: str
        """
        return self._operation

    @operation.setter
    def operation(self, operation):
        """
        Sets the operation of this SummaryProtocolProtocolItem.
        The operation performed.

        :param operation: The operation of this SummaryProtocolProtocolItem.
        :type: str
        """
        
        self._operation = operation

    @property
    def operation_count(self):
        """
        Gets the operation_count of this SummaryProtocolProtocolItem.
        The number of times an operation has been performed.

        :return: The operation_count of this SummaryProtocolProtocolItem.
        :rtype: int
        """
        return self._operation_count

    @operation_count.setter
    def operation_count(self, operation_count):
        """
        Sets the operation_count of this SummaryProtocolProtocolItem.
        The number of times an operation has been performed.

        :param operation_count: The operation_count of this SummaryProtocolProtocolItem.
        :type: int
        """
        
        self._operation_count = operation_count

    @property
    def operation_rate(self):
        """
        Gets the operation_rate of this SummaryProtocolProtocolItem.
        The rate (in ops/second) at which an operation has been performed.

        :return: The operation_rate of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._operation_rate

    @operation_rate.setter
    def operation_rate(self, operation_rate):
        """
        Sets the operation_rate of this SummaryProtocolProtocolItem.
        The rate (in ops/second) at which an operation has been performed.

        :param operation_rate: The operation_rate of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._operation_rate = operation_rate

    @property
    def out(self):
        """
        Gets the out of this SummaryProtocolProtocolItem.
        Rate of output (in bytes/second) for an operation since the last time isi statistics collected the data.

        :return: The out of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._out

    @out.setter
    def out(self, out):
        """
        Sets the out of this SummaryProtocolProtocolItem.
        Rate of output (in bytes/second) for an operation since the last time isi statistics collected the data.

        :param out: The out of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._out = out

    @property
    def out_avg(self):
        """
        Gets the out_avg of this SummaryProtocolProtocolItem.
        Average output (sent) bytes for an operation, in bytes.

        :return: The out_avg of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._out_avg

    @out_avg.setter
    def out_avg(self, out_avg):
        """
        Sets the out_avg of this SummaryProtocolProtocolItem.
        Average output (sent) bytes for an operation, in bytes.

        :param out_avg: The out_avg of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._out_avg = out_avg

    @property
    def out_max(self):
        """
        Gets the out_max of this SummaryProtocolProtocolItem.
        Maximum output (sent) bytes for an operation, in bytes.

        :return: The out_max of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._out_max

    @out_max.setter
    def out_max(self, out_max):
        """
        Sets the out_max of this SummaryProtocolProtocolItem.
        Maximum output (sent) bytes for an operation, in bytes.

        :param out_max: The out_max of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._out_max = out_max

    @property
    def out_min(self):
        """
        Gets the out_min of this SummaryProtocolProtocolItem.
        Minimum output (sent) bytes for an operation, in bytes.

        :return: The out_min of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._out_min

    @out_min.setter
    def out_min(self, out_min):
        """
        Sets the out_min of this SummaryProtocolProtocolItem.
        Minimum output (sent) bytes for an operation, in bytes.

        :param out_min: The out_min of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._out_min = out_min

    @property
    def out_standard_dev(self):
        """
        Gets the out_standard_dev of this SummaryProtocolProtocolItem.
        Standard deviation for output (received) bytes for an operation, in bytes.

        :return: The out_standard_dev of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._out_standard_dev

    @out_standard_dev.setter
    def out_standard_dev(self, out_standard_dev):
        """
        Sets the out_standard_dev of this SummaryProtocolProtocolItem.
        Standard deviation for output (received) bytes for an operation, in bytes.

        :param out_standard_dev: The out_standard_dev of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._out_standard_dev = out_standard_dev

    @property
    def protocol(self):
        """
        Gets the protocol of this SummaryProtocolProtocolItem.
        The protocol of the operation.

        :return: The protocol of this SummaryProtocolProtocolItem.
        :rtype: str
        """
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        """
        Sets the protocol of this SummaryProtocolProtocolItem.
        The protocol of the operation.

        :param protocol: The protocol of this SummaryProtocolProtocolItem.
        :type: str
        """
        
        self._protocol = protocol

    @property
    def time(self):
        """
        Gets the time of this SummaryProtocolProtocolItem.
        Unix Epoch time in seconds of the request.

        :return: The time of this SummaryProtocolProtocolItem.
        :rtype: int
        """
        return self._time

    @time.setter
    def time(self, time):
        """
        Sets the time of this SummaryProtocolProtocolItem.
        Unix Epoch time in seconds of the request.

        :param time: The time of this SummaryProtocolProtocolItem.
        :type: int
        """
        
        self._time = time

    @property
    def time_avg(self):
        """
        Gets the time_avg of this SummaryProtocolProtocolItem.
        The average elapsed time (in microseconds) taken to complete an operation.

        :return: The time_avg of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._time_avg

    @time_avg.setter
    def time_avg(self, time_avg):
        """
        Sets the time_avg of this SummaryProtocolProtocolItem.
        The average elapsed time (in microseconds) taken to complete an operation.

        :param time_avg: The time_avg of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._time_avg = time_avg

    @property
    def time_max(self):
        """
        Gets the time_max of this SummaryProtocolProtocolItem.
        The maximum elapsed time (in microseconds) taken to complete an operation.

        :return: The time_max of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._time_max

    @time_max.setter
    def time_max(self, time_max):
        """
        Sets the time_max of this SummaryProtocolProtocolItem.
        The maximum elapsed time (in microseconds) taken to complete an operation.

        :param time_max: The time_max of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._time_max = time_max

    @property
    def time_min(self):
        """
        Gets the time_min of this SummaryProtocolProtocolItem.
        The minimum elapsed time (in microseconds) taken to complete an operation.

        :return: The time_min of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._time_min

    @time_min.setter
    def time_min(self, time_min):
        """
        Sets the time_min of this SummaryProtocolProtocolItem.
        The minimum elapsed time (in microseconds) taken to complete an operation.

        :param time_min: The time_min of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._time_min = time_min

    @property
    def time_standard_dev(self):
        """
        Gets the time_standard_dev of this SummaryProtocolProtocolItem.
        The standard deviation time (in microseconds) taken to complete an operation.

        :return: The time_standard_dev of this SummaryProtocolProtocolItem.
        :rtype: float
        """
        return self._time_standard_dev

    @time_standard_dev.setter
    def time_standard_dev(self, time_standard_dev):
        """
        Sets the time_standard_dev of this SummaryProtocolProtocolItem.
        The standard deviation time (in microseconds) taken to complete an operation.

        :param time_standard_dev: The time_standard_dev of this SummaryProtocolProtocolItem.
        :type: float
        """
        
        self._time_standard_dev = time_standard_dev

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

