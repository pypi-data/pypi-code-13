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


class NodeDrivesNodeDrive(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        NodeDrivesNodeDrive - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'baynum': 'int',
            'blocks': 'int',
            'chassis': 'int',
            'devname': 'str',
            'firmware': 'NodeDrivesNodeDriveFirmware',
            'handle': 'int',
            'interface_type': 'str',
            'lnum': 'int',
            'locnstr': 'str',
            'logical_block_length': 'int',
            'media_type': 'str',
            'model': 'str',
            'physical_block_length': 'int',
            'present': 'bool',
            'purpose': 'str',
            'purpose_description': 'str',
            'serial': 'str',
            'ui_state': 'str',
            'wwn': 'str',
            'x_loc': 'int',
            'y_loc': 'int'
        }

        self.attribute_map = {
            'baynum': 'baynum',
            'blocks': 'blocks',
            'chassis': 'chassis',
            'devname': 'devname',
            'firmware': 'firmware',
            'handle': 'handle',
            'interface_type': 'interface_type',
            'lnum': 'lnum',
            'locnstr': 'locnstr',
            'logical_block_length': 'logical_block_length',
            'media_type': 'media_type',
            'model': 'model',
            'physical_block_length': 'physical_block_length',
            'present': 'present',
            'purpose': 'purpose',
            'purpose_description': 'purpose_description',
            'serial': 'serial',
            'ui_state': 'ui_state',
            'wwn': 'wwn',
            'x_loc': 'x_loc',
            'y_loc': 'y_loc'
        }

        self._baynum = None
        self._blocks = None
        self._chassis = None
        self._devname = None
        self._firmware = None
        self._handle = None
        self._interface_type = None
        self._lnum = None
        self._locnstr = None
        self._logical_block_length = None
        self._media_type = None
        self._model = None
        self._physical_block_length = None
        self._present = None
        self._purpose = None
        self._purpose_description = None
        self._serial = None
        self._ui_state = None
        self._wwn = None
        self._x_loc = None
        self._y_loc = None

    @property
    def baynum(self):
        """
        Gets the baynum of this NodeDrivesNodeDrive.
        Numerical representation of this drive's bay.

        :return: The baynum of this NodeDrivesNodeDrive.
        :rtype: int
        """
        return self._baynum

    @baynum.setter
    def baynum(self, baynum):
        """
        Sets the baynum of this NodeDrivesNodeDrive.
        Numerical representation of this drive's bay.

        :param baynum: The baynum of this NodeDrivesNodeDrive.
        :type: int
        """
        
        self._baynum = baynum

    @property
    def blocks(self):
        """
        Gets the blocks of this NodeDrivesNodeDrive.
        Number of blocks on this drive.

        :return: The blocks of this NodeDrivesNodeDrive.
        :rtype: int
        """
        return self._blocks

    @blocks.setter
    def blocks(self, blocks):
        """
        Sets the blocks of this NodeDrivesNodeDrive.
        Number of blocks on this drive.

        :param blocks: The blocks of this NodeDrivesNodeDrive.
        :type: int
        """
        
        self._blocks = blocks

    @property
    def chassis(self):
        """
        Gets the chassis of this NodeDrivesNodeDrive.
        The chassis number which contains this drive.

        :return: The chassis of this NodeDrivesNodeDrive.
        :rtype: int
        """
        return self._chassis

    @chassis.setter
    def chassis(self, chassis):
        """
        Sets the chassis of this NodeDrivesNodeDrive.
        The chassis number which contains this drive.

        :param chassis: The chassis of this NodeDrivesNodeDrive.
        :type: int
        """
        
        self._chassis = chassis

    @property
    def devname(self):
        """
        Gets the devname of this NodeDrivesNodeDrive.
        This drive's device name.

        :return: The devname of this NodeDrivesNodeDrive.
        :rtype: str
        """
        return self._devname

    @devname.setter
    def devname(self, devname):
        """
        Sets the devname of this NodeDrivesNodeDrive.
        This drive's device name.

        :param devname: The devname of this NodeDrivesNodeDrive.
        :type: str
        """
        
        self._devname = devname

    @property
    def firmware(self):
        """
        Gets the firmware of this NodeDrivesNodeDrive.
        Drive firmware information.

        :return: The firmware of this NodeDrivesNodeDrive.
        :rtype: NodeDrivesNodeDriveFirmware
        """
        return self._firmware

    @firmware.setter
    def firmware(self, firmware):
        """
        Sets the firmware of this NodeDrivesNodeDrive.
        Drive firmware information.

        :param firmware: The firmware of this NodeDrivesNodeDrive.
        :type: NodeDrivesNodeDriveFirmware
        """
        
        self._firmware = firmware

    @property
    def handle(self):
        """
        Gets the handle of this NodeDrivesNodeDrive.
        Drive_d's handle representation for this drive

        :return: The handle of this NodeDrivesNodeDrive.
        :rtype: int
        """
        return self._handle

    @handle.setter
    def handle(self, handle):
        """
        Sets the handle of this NodeDrivesNodeDrive.
        Drive_d's handle representation for this drive

        :param handle: The handle of this NodeDrivesNodeDrive.
        :type: int
        """
        
        self._handle = handle

    @property
    def interface_type(self):
        """
        Gets the interface_type of this NodeDrivesNodeDrive.
        String representtation of this drive's interface type.

        :return: The interface_type of this NodeDrivesNodeDrive.
        :rtype: str
        """
        return self._interface_type

    @interface_type.setter
    def interface_type(self, interface_type):
        """
        Sets the interface_type of this NodeDrivesNodeDrive.
        String representtation of this drive's interface type.

        :param interface_type: The interface_type of this NodeDrivesNodeDrive.
        :type: str
        """
        
        self._interface_type = interface_type

    @property
    def lnum(self):
        """
        Gets the lnum of this NodeDrivesNodeDrive.
        This drive's logical drive number in IFS.

        :return: The lnum of this NodeDrivesNodeDrive.
        :rtype: int
        """
        return self._lnum

    @lnum.setter
    def lnum(self, lnum):
        """
        Sets the lnum of this NodeDrivesNodeDrive.
        This drive's logical drive number in IFS.

        :param lnum: The lnum of this NodeDrivesNodeDrive.
        :type: int
        """
        
        self._lnum = lnum

    @property
    def locnstr(self):
        """
        Gets the locnstr of this NodeDrivesNodeDrive.
        String representation of this drive's physical location.

        :return: The locnstr of this NodeDrivesNodeDrive.
        :rtype: str
        """
        return self._locnstr

    @locnstr.setter
    def locnstr(self, locnstr):
        """
        Sets the locnstr of this NodeDrivesNodeDrive.
        String representation of this drive's physical location.

        :param locnstr: The locnstr of this NodeDrivesNodeDrive.
        :type: str
        """
        
        self._locnstr = locnstr

    @property
    def logical_block_length(self):
        """
        Gets the logical_block_length of this NodeDrivesNodeDrive.
        Size of a logical block on this drive.

        :return: The logical_block_length of this NodeDrivesNodeDrive.
        :rtype: int
        """
        return self._logical_block_length

    @logical_block_length.setter
    def logical_block_length(self, logical_block_length):
        """
        Sets the logical_block_length of this NodeDrivesNodeDrive.
        Size of a logical block on this drive.

        :param logical_block_length: The logical_block_length of this NodeDrivesNodeDrive.
        :type: int
        """
        
        self._logical_block_length = logical_block_length

    @property
    def media_type(self):
        """
        Gets the media_type of this NodeDrivesNodeDrive.
        String representation of this drive's media type.

        :return: The media_type of this NodeDrivesNodeDrive.
        :rtype: str
        """
        return self._media_type

    @media_type.setter
    def media_type(self, media_type):
        """
        Sets the media_type of this NodeDrivesNodeDrive.
        String representation of this drive's media type.

        :param media_type: The media_type of this NodeDrivesNodeDrive.
        :type: str
        """
        
        self._media_type = media_type

    @property
    def model(self):
        """
        Gets the model of this NodeDrivesNodeDrive.
        This drive's manufacturer and model.

        :return: The model of this NodeDrivesNodeDrive.
        :rtype: str
        """
        return self._model

    @model.setter
    def model(self, model):
        """
        Sets the model of this NodeDrivesNodeDrive.
        This drive's manufacturer and model.

        :param model: The model of this NodeDrivesNodeDrive.
        :type: str
        """
        
        self._model = model

    @property
    def physical_block_length(self):
        """
        Gets the physical_block_length of this NodeDrivesNodeDrive.
        Size of a physical block on this drive.

        :return: The physical_block_length of this NodeDrivesNodeDrive.
        :rtype: int
        """
        return self._physical_block_length

    @physical_block_length.setter
    def physical_block_length(self, physical_block_length):
        """
        Sets the physical_block_length of this NodeDrivesNodeDrive.
        Size of a physical block on this drive.

        :param physical_block_length: The physical_block_length of this NodeDrivesNodeDrive.
        :type: int
        """
        
        self._physical_block_length = physical_block_length

    @property
    def present(self):
        """
        Gets the present of this NodeDrivesNodeDrive.
        Indicates whether this drive is physically present in the node.

        :return: The present of this NodeDrivesNodeDrive.
        :rtype: bool
        """
        return self._present

    @present.setter
    def present(self, present):
        """
        Sets the present of this NodeDrivesNodeDrive.
        Indicates whether this drive is physically present in the node.

        :param present: The present of this NodeDrivesNodeDrive.
        :type: bool
        """
        
        self._present = present

    @property
    def purpose(self):
        """
        Gets the purpose of this NodeDrivesNodeDrive.
        This drive's purpose in the DRV state machine.

        :return: The purpose of this NodeDrivesNodeDrive.
        :rtype: str
        """
        return self._purpose

    @purpose.setter
    def purpose(self, purpose):
        """
        Sets the purpose of this NodeDrivesNodeDrive.
        This drive's purpose in the DRV state machine.

        :param purpose: The purpose of this NodeDrivesNodeDrive.
        :type: str
        """
        
        self._purpose = purpose

    @property
    def purpose_description(self):
        """
        Gets the purpose_description of this NodeDrivesNodeDrive.
        Description of this drive's purpose.

        :return: The purpose_description of this NodeDrivesNodeDrive.
        :rtype: str
        """
        return self._purpose_description

    @purpose_description.setter
    def purpose_description(self, purpose_description):
        """
        Sets the purpose_description of this NodeDrivesNodeDrive.
        Description of this drive's purpose.

        :param purpose_description: The purpose_description of this NodeDrivesNodeDrive.
        :type: str
        """
        
        self._purpose_description = purpose_description

    @property
    def serial(self):
        """
        Gets the serial of this NodeDrivesNodeDrive.
        Serial number for this drive.

        :return: The serial of this NodeDrivesNodeDrive.
        :rtype: str
        """
        return self._serial

    @serial.setter
    def serial(self, serial):
        """
        Sets the serial of this NodeDrivesNodeDrive.
        Serial number for this drive.

        :param serial: The serial of this NodeDrivesNodeDrive.
        :type: str
        """
        
        self._serial = serial

    @property
    def ui_state(self):
        """
        Gets the ui_state of this NodeDrivesNodeDrive.
        This drive's state as presented to the UI.

        :return: The ui_state of this NodeDrivesNodeDrive.
        :rtype: str
        """
        return self._ui_state

    @ui_state.setter
    def ui_state(self, ui_state):
        """
        Sets the ui_state of this NodeDrivesNodeDrive.
        This drive's state as presented to the UI.

        :param ui_state: The ui_state of this NodeDrivesNodeDrive.
        :type: str
        """
        
        self._ui_state = ui_state

    @property
    def wwn(self):
        """
        Gets the wwn of this NodeDrivesNodeDrive.
        The drive's 'worldwide name' from its NAA identifiers.

        :return: The wwn of this NodeDrivesNodeDrive.
        :rtype: str
        """
        return self._wwn

    @wwn.setter
    def wwn(self, wwn):
        """
        Sets the wwn of this NodeDrivesNodeDrive.
        The drive's 'worldwide name' from its NAA identifiers.

        :param wwn: The wwn of this NodeDrivesNodeDrive.
        :type: str
        """
        
        self._wwn = wwn

    @property
    def x_loc(self):
        """
        Gets the x_loc of this NodeDrivesNodeDrive.
        This drive's x-axis grid location.

        :return: The x_loc of this NodeDrivesNodeDrive.
        :rtype: int
        """
        return self._x_loc

    @x_loc.setter
    def x_loc(self, x_loc):
        """
        Sets the x_loc of this NodeDrivesNodeDrive.
        This drive's x-axis grid location.

        :param x_loc: The x_loc of this NodeDrivesNodeDrive.
        :type: int
        """
        
        self._x_loc = x_loc

    @property
    def y_loc(self):
        """
        Gets the y_loc of this NodeDrivesNodeDrive.
        This drive's y-axis grid location.

        :return: The y_loc of this NodeDrivesNodeDrive.
        :rtype: int
        """
        return self._y_loc

    @y_loc.setter
    def y_loc(self, y_loc):
        """
        Sets the y_loc of this NodeDrivesNodeDrive.
        This drive's y-axis grid location.

        :param y_loc: The y_loc of this NodeDrivesNodeDrive.
        :type: int
        """
        
        self._y_loc = y_loc

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

