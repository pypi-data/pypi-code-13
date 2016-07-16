# EventMaster Library for Python
# Unofficial Python Library for connecting to, reading from and controlling
# a Barco E2, S3 or other EventMaster Switcher
# Author: Kye Lewis <klewis@stagingconnections.com>
# GitHub: http://github.com/kyelewisstgc/pye2s3/

# Version: 160716.a

import socket
import re
from threading import Thread
from threading import Timer
from uuid import uuid4
from time import sleep
from math import ceil

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# Globals
global SDI_TYPE_SD
global SDI_TYPE_HD
global SDI_TYPE_LEVELA
global SDI_TYPE_LEVELB
SDI_TYPE_SD = 0
SDI_TYPE_HD = 1
SDI_TYPE_LEVELA = 2
SDI_TYPE_LEVELB = 3

global COLORSPACE_RGB
global COLORSPACE_SMPTE
COLORSPACE_RGB = 0
COLORSPACE_SMPTE = 1

global BLACKONINVALID_ON
global BLACKONINVALID_OFF
BLACKONINVALID_OFF = 0
BLACKONINVALID_ON = 1

global COLORRANGE_REDUCED
global COLORRANGE_FULL
COLORRANGE_REDUCED = 0
COLORRANGE_FULL = 1

global VF_1024x768_4795
global VF_1024x768_4800
global VF_1024x768_5000
global VF_1024x768_5994
global VF_1024x768_6000
global VF_1024x768_7000
global VF_1024x768_7193
global VF_1024x768_7200
global VF_1024x768_7500
global VF_1024x768_8500
VF_1024x768_4795 = 700
VF_1024x768_4800 = 701
VF_1024x768_5000 = 702
VF_1024x768_5994 = 703
VF_1024x768_6000 = 704
VF_1024x768_7000 = 705
VF_1024x768_7193 = 706
VF_1024x768_7200 = 707
VF_1024x768_7500 = 708
VF_1024x768_8500 = 709

global VF_1152x864_7500
VF_1152x864_7500 = 900

global VF_1280x1024_4795
global VF_1280x1024_4800
global VF_1280x1024_5000
global VF_1280x1024_5994
global VF_1280x1024_6000
global VF_1280x1024_7000
global VF_1280x1024_7193
global VF_1280x1024_7200
global VF_1280x1024_7500
global VF_1280x1024_8500
VF_1280x1024_4795 = 1500
VF_1280x1024_4800 = 1501
VF_1280x1024_5000 = 1502
VF_1280x1024_5994 = 1503
VF_1280x1024_6000 = 1504
VF_1280x1024_7000 = 1505
VF_1280x1024_7193 = 1506
VF_1280x1024_7200 = 1507
VF_1280x1024_7500 = 1508
VF_1280x1024_8500 = 1509

global VF_1280x720p_2398
global VF_1280x720p_2400
global VF_1280x720p_2500
global VF_1280x720p_2997
global VF_1280x720p_3000
global VF_1280x720p_4800
global VF_1280x720p_5000
global VF_1280x720p_5994
global VF_1280x720p_6000
global VF_1280x720p_10000
global VF_1280x720p_11988
global VF_1280x720p_12000
VF_1280x720p_2398 = 1000
VF_1280x720p_2400 = 1001
VF_1280x720p_2500 = 1002
VF_1280x720p_2997 = 1003
VF_1280x720p_3000 = 1004
VF_1280x720p_4800 = 1005
VF_1280x720p_5000 = 1006
VF_1280x720p_5994 = 1007
VF_1280x720p_6000 = 1008
VF_1280x720p_10000 = 1013
VF_1280x720p_11988 = 1014
VF_1280x720p_12000 = 1015

global VF_1920x1080p_2398
global VF_1920x1080p_2400
global VF_1920x1080p_2500
global VF_1920x1080p_2997
global VF_1920x1080p_3000
global VF_1920x1080p_4795
global VF_1920x1080p_4800
global VF_1920x1080p_5000
global VF_1920x1080p_5994
global VF_1920x1080p_6000
VF_1920x1080p_2398 = 2700
VF_1920x1080p_2400 = 2701
VF_1920x1080p_2500 = 2702
VF_1920x1080p_2997 = 2703
VF_1920x1080p_3000 = 2704
VF_1920x1080p_4795 = 2705
VF_1920x1080p_4800 = 2706
VF_1920x1080p_5000 = 2707
VF_1920x1080p_5994 = 2708
VF_1920x1080p_6000 = 2709

global VF_1920x1080i_5000
global VF_1920x1080i_5994
global VF_1920x1080i_6000
VF_1920x1080i_5000 = 2900
VF_1920x1080i_5994 = 2901
VF_1920x1080i_6000 = 2902

global HDCPMODE_ON
global HDCPMODE_OFF
HDCPMODE_ON = 1
HDCPMODE_OFF = 0

global FRZMODE_ON
global FRZMODE_OFF
FRZMODE_ON = 1
FRZMODE_OFF = 0

global AUXSTREAMMODE_2K
global AUXSTREAMMODE_DL
global AUXSTREAMMODE_4K
global AUXSTREAMMODE_8L
AUXSTREAMMODE_2K = 1
AUXSTREAMMODE_DL = 2
AUXSTREAMMODE_4K = 4
AUXSTREAMMODE_8L = 8

global TESTPATTERNMODE_OFF
global TESTPATTERNMODE_HRAMP
global TESTPATTERNMODE_VRAMP
global TESTPATTERNMODE_CBAR100
global TESTPATTERNMODE_GRID16
global TESTPATTERNMODE_GRID32
global TESTPATTERNMODE_BURST
global TESTPATTERNMODE_CBAR75
global TESTPATTERNMODE_GRAY50
global TESTPATTERNMODE_HSTEPS
global TESTPATTERNMODE_VSTEPS
global TESTPATTERNMODE_WHITE
global TESTPATTERNMODE_BLACK
global TESTPATTERNMODE_SMPTE
global TESTPATTERNMODE_HALIGN
global TESTPATTERNMODE_VALIGN
global TESTPATTERNMODE_HVALIGN
TESTPATTERNMODE_OFF = 0
TESTPATTERNMODE_HRAMP = 1
TESTPATTERNMODE_VRAMP = 2
TESTPATTERNMODE_CBAR100 = 3
TESTPATTERNMODE_GRID16 = 4
TESTPATTERNMODE_GRID32 = 5
TESTPATTERNMODE_BURST = 6
TESTPATTERNMODE_CBAR75 = 7
TESTPATTERNMODE_GRAY50 = 8
TESTPATTERNMODE_HSTEPS = 9
TESTPATTERNMODE_VSTEPS = 10
TESTPATTERNMODE_WHITE = 11
TESTPATTERNMODE_BLACK = 12
TESTPATTERNMODE_SMPTE = 13
TESTPATTERNMODE_HALIGN = 14
TESTPATTERNMODE_VALIGN = 15
TESTPATTERNMODE_HVALIGN = 16

global RASTERBOX_ON
global RASTERBOX_OFF
RASTERBOX_ON = 1
RASTERBOX_OFF = 0

global DIAGMOTION_ON
global DIAGMOTION_OFF
DIAGMOTION_ON = 1
DIAGMOTION_OFF = 0

global CONNCAPACITY_NONE
global CONNCAPACITY_SL
CONNCAPACITY_NONE = 0
CONNCAPACITY_SL = 1


class EventMasterBase(object):

    def _log(self, logtext_string):
        """Log to the console or logfile"""
        if not logtext_string: return -1
        class_name_string = self.__class__.__name__

        if(hasattr(self, "parent")):
            if(self.parent.getVerbose()==1):
                print("[{0!s}] {1!s}".format(class_name_string, logtext_string))

        else:
            if(self.getVerbose()==1):
                print("[{0!s}] {1!s}".format(class_name_string, logtext_string))

        return 1


class EventMasterCollection(EventMasterBase):

    def __init__(self, parent):
        """Generic Init"""
        self.parent = parent
        self.state = {}

    def update_state(self, state_dict):
        """Update state dict values"""
        for key, val in state_dict.items():
            self.state[key] = val
        return 1

    def _simple_set(self, key_string, value, xml_path_list=None):
        """Set a basic XML value"""
        xml_path_open_string = ""
        xml_path_close_string = ""

        if((xml_path_list != None) and (type(xml_path_list)==list)):
            for item in xml_path_list:
                xml_path_open_string += "<{0!s}>".format(item)
            for item in xml_path_list[::-1]:
                xml_path_close_string += "</{0!s}>".format(item.split(' ', 1)[0])

        value_string = str(value)
        xml_string = "{0!s}<{1!s}>{2!s}</{1!s}>{3!s}".format(xml_path_open_string, key_string, value_string, xml_path_close_string)
        return self.send(xml_string)

    def _simple_get(self, key_string):
        """Get a basic value from state dict"""
        if key_string not in self.state:
            return None

        return self.state[key_string]

    def send(self, xml_string):
        """Send a basic XML string"""
        xml_path_open_string = ""
        xml_path_close_string = ""
        for item in self.xml_path_list:
            xml_path_open_string += "<{0!s}>".format(item)
        for item in self.xml_path_list[::-1]:
            xml_path_close_string += "</{0!s}>".format(item.split(' ', 1)[0])

        xml_ext_string = "{0!s}{1!s}{2!s}".format(str(xml_path_open_string),
                                                  str(xml_string),
                                                  str(xml_path_close_string))
        return self.parent.send(str(xml_ext_string))


class EventMasterLayer(EventMasterCollection):

    def __init__(self, parent, layer_int, destination_int, state_dict={}):
        """Create a new Layer Instance

        Keyword arguments:
        layer_int -- Unique Layer ID number
        destination_int -- The destination ID number the layer is assigned to
        state_dict -- Optional, a dict of Layer state items as defined below
        """

        super(EventMasterLayer, self).__init__(parent)

        if parent is None:
            raise Exception( "EventMasterInput init - parent must be supplied" )

        if destination_int is None or type(destination_int) != int:
            raise Exception( "EventMasterLayer init - Destination must be supplied and must be an Integer" )
            return

        if layer_int is None or type(layer_int) != int:
            raise Exception( "EventMasterLayer init - Layer must be supplied and must be an Integer" )
            return

        self.layer = layer_int
        self.destination = destination_int
        self.state = state_dict

        self.xml_path_list = [  "DestMgr id=\"0\"",
                                "ScreenDestCol id=\"0\"",
                                "ScreenDest id=\"{0!s}\"".format(self.destination),
                                "LayerCollection id=\"0\"",
                                "Layer id=\"{0!s}".format(self.layer),
                                "LayerCfg id=\"0\""      ]

        return

    def getName(self):
        """(string) Gets Layer Name"""
        return self._simple_get("Name")

    def getPvwMode(self):
        return self._simple_get("PvwMode")

    def getPgmMode(self):
        return self._simple_get("PgmMode")

    def getOWIN(self):
        """(dict) Gets Layer Outside Window Position & Size"""
        owin_dict = {}
        owin_dict["HPos"] = self._simple_get("OWIN_HPos")
        owin_dict["VPos"] = self._simple_get("OWIN_VPos")
        owin_dict["HSize"] = self._simple_get("OWIN_HSize")
        owin_dict["VSize"] = self._simple_get("OWIN_VSize")
        return owin_dict

    def setOWIN(self, HPos=None, VPos=None, HSize=None, VSize=None):
        """ Sets Layer Outside Window Position & Size
            Returns None

            (int)HPos -- Horizontal Position in pixels
            (int)VPos -- Vertical Position in pixels
            (int)HSize -- Horizontal Size in pixels
            (int)VSize -- Vertical Size in pixels
        """

        xml_path_list = ["LayerState id=\"0\"",
                         "WinAdjust id=\"0\"",
                         "PostMaskOWIN id=\"0\""]

        if HPos and type(HPos) == int:
            self._simple_set("HPosCmd", HPos, xml_path_list=xml_path_list)

        if VPos and type(VPos) == int:
            self._simple_set("VPosCmd", VPos, xml_path_list=xml_path_list)

        if HSize and type(HSize) == int:
            self._simple_set("HSizeCmd", HSize, xml_path_list=xml_path_list)

        if VSize and type(VSize) == int:
            self._simple_set("VSizeCmd", VSize, xml_path_list=xml_path_list)

    def cmdFreeze(self, freeze_int):
        """ Sets Layer Freeze Mode On/Off
            Returns a unique query UUID as string
            Args:   (int)freeze_int -- Freeze (FRZMODE_ON, FRZMODE_OFF) """

        if freeze_int is not None or type(freeze_int) != int: return None
        if freeze_int != FRZMODE_ON and freeze_int != FRZMODE_OFF: return None

        return self._simple_set("FrzCmd", freeze_int)

    def getFreeze(self):
        """ Gets Layer Freeze Mode
            Returns FRZMODE_ON or FRZMODE_OFF """
        return self._simple_get("FrzMode")

    def toggleFreeze(self):
        """ Toggles Layer Freeze Mode
            Returns a unique query UUID as string """
        frz_int = self.getFreeze()
        if(frz_int == FRZMODE_ON):
            return self.cmdFreeze(FRZMODE_OFF)
        elif(frz_int == FRZMODE_OFF):
            return self.cmdFreeze(FRZMODE_ON)
        else:
            return None

    def getSource(self):
        src = self._simple_get("Source")
        src_type = self._simple_get("SrcType")

        """ SrcType 0 is Input Source """
        if(src_type == 0):
            if src in self.parent.inputs:
                return self.parent.inputs[src]
        return None


    def cmdRouteSource(self, source_int):
        if not source_int or type(source_int) != int:
            return None

        """ TODO: Check if source is valid """
        return self._simple_set("SrcIdx", source_int)


    def cmdApplyUserKey(self, userkey_int):
        if userkey_int is None:
            return None
        return self._simple_set("ApplyUserKey", userkey_int)


class EventMasterScreenDestination(EventMasterCollection):

    def __init__(self, parent, destination_int, state_dict={}):
        """ Create a new Screen Destination Instance
            Returns an instance of EventMasterScreenDestination
            Args:   (object)parent -- EventMasterSwitcher instance
                    (int)input_int - Unique Destination ID number
                    optional (dict)state_dict -- Dict of state items """

        super(EventMasterScreenDestination, self).__init__(parent)

        if parent is None:
            raise Exception( "EventMasterInput init - parent must be supplied" )

        if destination_int is None or type(destination_int) != int:
            raise Exception( "EventMasterInput init - destination_int must be supplied and must be an Integer" )

        self.destination = destination_int
        self.state = state_dict
        self.layers = {}

        self.xml_path_list = [ "DestMgr id=\"0\"",
                               "ScreenDestCol id=\"0\"",
                               "ScreenDest id=\"{0!s}\"".format(self.destination)    ]

        return

    def getName(self):
        return self._simple_get("Name")

    def getSize(self):
        return { "HSize": self._simple_get("HSize"),
                 "VSize": self._simple_get("VSize") }

    def getLayers(self):
        if not self.layers.items:
            return {}

        layers = {}

        for key, inst in self.layers.items():
            real_layer_number = int(ceil(key/2))
            if real_layer_number not in layers:
                layers[real_layer_number] = {}
            if inst.getPvwMode():
                layers[real_layer_number]["Pvw"] = inst
            if inst.getPgmMode():
                layers[real_layer_number]["Pgm"] = inst

        return layers

    def _updateLayer(self, layer_int, state_dict):
        if layer_int in self.layers:
            self.layers[layer_int].update_state(state_dict)
        else:
            self.layers[layer_int] = EventMasterLayer( self.parent,
                                                       layer_int=layer_int,
                                                       destination_int=self.destination,
                                                       state_dict=state_dict)
        return 1


class EventMasterOutput(EventMasterCollection):

    def __init__(self, parent, output_int, state_dict={}):
        """ Create a new Output Instance
            Returns an instance of EventMasterOutput
            Args:   (object)parent -- EventMasterSwitcher instance
                    (int)output_int - Unique Output ID number
                    optional (dict)state_dict -- Dict of state items """

        super(EventMasterOutput, self).__init__(parent)

        if parent is None:
            raise Exception( "EventMasterOutput init - parent must be supplied" )

        if output_int is None or type(output_int) != int:
            raise Exception( "EventMasterOutput init - output_int must be supplied and must be an Integer" )

        self.output = output_int
        self.state = state_dict

        self.xml_path_list = [ "OutCfgMgr id=\"0\"",
                               "OutputCfg id=\"{0!s}\"".format(self.output)    ]

        return

    def getName(self):
        return self._simple_get("Name")

    def getTestPatternMode(self):
        return self._simple_get("TestPattern_Mode")

    def getRasterBox(self):
        return self._simple_get("TestPattern_RasterBox")

    def getTestPatternDiagMotion(self):
        return self._simple_get("TestPattern_DiagMotion")


class EventMasterPreset(EventMasterCollection):

    def __init__(self, parent, preset_int, state_dict={}):
        """ Create a new Preset Instance
            Returns an instance of EventMasterPreset
            Args:   (object)parent -- EventMasterSwitcher instance
                    (int)output_int - Unique Preset ID number
                    optional (dict)state_dict -- Dict of state items """

        super(EventMasterPreset, self).__init__(parent)

        if parent is None:
            raise Exception( "EventMasterPreset init - parent must be supplied" )

        if preset_int is None or type(preset_int) != int:
            raise Exception( "EventMasterPreset init - preset_int must be supplied and must be an Integer" )

        self.preset = preset_int
        self.state = state_dict

        self.xml_path_list = [ "PresetMgr id=\"0\"",
                               "Preset id=\"{0!s}\"".format(self.preset)  ]

        return

    def getName(self):
        return self._simple_get("Name")

    def setName(self, name_string):
        if name_string is None or type(name_string) != str:
            return None
        return self._simple_set("Name")

    def cmdRecall(self):
        xml = "<PresetMgr><RecallPreset>{0!s}</RecallPreset></PresetMgr>".format(self.preset)
        return self.parent.send(xml)


class EventMasterInput(EventMasterCollection):

    # S3 Default Input Map.
    # TODO: Get this from unit
    S3_DEFAULT_INPUT_MAP = {
    	1: {"conn_index": "0", "slot_index": "3",
            "card_type": "1", "frame_connector_type": "SDI"},
        2: {"conn_index": "1", "slot_index": "3",
            "card_type": "1", "frame_connector_type": "SDI"},
        3: {"conn_index": "2", "slot_index": "3",
            "card_type": "1", "frame_connector_type": "SDI"},
        4: {"conn_index": "3", "slot_index": "3",
            "card_type": "1", "frame_connector_type": "SDI"},
        5: {"conn_index": "0", "slot_index": "4",
            "card_type": "2", "frame_connector_type": "DP"},
        6: {"conn_index": "1", "slot_index": "4",
            "card_type": "2", "frame_connector_type": "DP"},
        7: {"conn_index": "2", "slot_index": "4",
            "card_type": "2", "frame_connector_type": "HDMI"},
        8: {"conn_index": "3", "slot_index": "4",
            "card_type": "2", "frame_connector_type": "HDMI"},
        9: {"conn_index": "0", "slot_index": "5",
            "card_type": "2", "frame_connector_type": "DP"},
        10: {"conn_index": "1", "slot_index": "5",
             "card_type": "2", "frame_connector_type": "DP"},
        11: {"conn_index": "2", "slot_index": "5",
             "card_type": "2", "frame_connector_type": "HDMI"},
        12: {"conn_index": "3", "slot_index": "5",
             "card_type": "2", "frame_connector_type": "HDMI"}
    }

    def __init__(self, parent, input_int, state_dict={}):
        """ Create a new Input Instance
            Returns an instance of EventMasterInput
            Args:   (object)parent -- EventMasterSwitcher instance
                    (int)input_int - Unique Input ID number
                    optional (dict)state_dict -- Dict of state items """

        super(EventMasterInput, self).__init__(parent)

        if parent is None:
            raise Exception( "EventMasterInput init - parent must be supplied" )

        if input_int is None or type(input_int) != int:
            raise Exception( "EventMasterInput init - input_int must be supplied and must be an Integer" )

        self.input = input_int
        self.state = state_dict

        self.xml_path_list = [ "SrcMgr id=\"0\"",
                               "InputCfgCol id=\"0\"",
                               "InputCfg id=\"{0!s}\"".format(self.input)    ]

        return

    def cmdFreeze(self, freeze_int):
        """ Sets Freeze Mode On/Off
            Returns a unique query UUID as string
            Args:   (int)freeze_int -- Freeze (FRZMODE_ON, FRZMODE_OFF) """

        if freeze_int is not None or type(freeze_int) != int: return None
        if freeze_int != FRZMODE_ON and freeze_int != FRZMODE_OFF: return None

        return self._simple_set("FrzCmd", freeze_int)

    def getFreeze(self):
        """ Gets Input Freeze Mode
            Returns FRZMODE_ON or FRZMODE_OFF """
        return self._simple_get("FrzMode")

    def toggleFreeze(self):
        """ Toggles Input Freeze Mode
            Returns a unique query UUID as string """
        frz_int = self.getFreeze()
        if(frz_int == FRZMODE_ON):
            return self.cmdFreeze(FRZMODE_OFF)
        elif(frz_int == FRZMODE_OFF):
            return self.cmdFreeze(FRZMODE_ON)
        else:
            return None

    def setName(self, name_string):
        """ Sets Input Name
            Returns a unique query UUID as string
            Args:   (str)name_string -- Input name """

        if name_string is not None or type(name_string) != str:
            return None

        return self._simple_set("Name", name_string)

    def getName(self):
        """(str) Gets Input Name"""
        return self._simple_get("Name")

    def getInputCfgType(self):
        """(int) Gets Input Configuration Type"""
        return self._simple_get("InputCfgType")

    def getAutoAcqMode(self):
        """(int) Gets Input Auto Acquire Mode Status"""
        return self._simple_get("AutoAcqMode")

    def getType3G(self):
        """(int) Gets Input 3G Type"""
        return self._simple_get("Type3G")


class EventMasterFrame(EventMasterCollection):

    # TODO: Complete VF List (or get from unit?)
    VF_MAP = {  1000: VF_1280x720p_2398,
                1001: VF_1280x720p_2400,
                1002: VF_1280x720p_2500,
                1003: VF_1280x720p_2997,
                1004: VF_1280x720p_3000,
                1005: VF_1280x720p_4800,
                1006: VF_1280x720p_5000,
                1007: VF_1280x720p_5994,
                1008: VF_1280x720p_6000,
                1013: VF_1280x720p_10000,
                1014: VF_1280x720p_11988,
                1015: VF_1280x720p_12000,
                2700: VF_1920x1080p_2398,
                2701: VF_1920x1080p_2400,
                2702: VF_1920x1080p_2500,
                2703: VF_1920x1080p_2997,
                2704: VF_1920x1080p_3000,
                2705: VF_1920x1080p_4795,
                2706: VF_1920x1080p_4800,
                2707: VF_1920x1080p_5000,
                2708: VF_1920x1080p_5994,
                2709: VF_1920x1080p_6000 }


    STR_MAP = { "1280x720p@23.98": VF_1280x720p_2398,
                "1280x720p@24": VF_1280x720p_2400,
                "1280x720p@25": VF_1280x720p_2500,
                "1280x720p@29.97": VF_1280x720p_2997,
                "1280x720p@30": VF_1280x720p_3000,
                "1280x720p@48": VF_1280x720p_4800,
                "1280x720p@50": VF_1280x720p_5000,
                "1280x720p@59.94": VF_1280x720p_5994,
                "1280x720p@60": VF_1280x720p_6000,
                "1280x720p@100": VF_1280x720p_10000,
                "1280x720p@119.88": VF_1280x720p_11988,
                "1280x720p@120": VF_1280x720p_12000,
                "1920x1080p@23.98": VF_1920x1080p_2398,
                "1920x1080p@24": VF_1920x1080p_2400,
                "1920x1080p@25": VF_1920x1080p_2500,
                "1920x1080p@29.97": VF_1920x1080p_2997,
                "1920x1080p@30": VF_1920x1080p_3000,
                "1920x1080p@47.95": VF_1920x1080p_4795,
                "1920x1080p@48": VF_1920x1080p_4800,
                "1920x1080p@50": VF_1920x1080p_5000,
                "1920x1080p@59.94": VF_1920x1080p_5994,
                "1920x1080p@60": VF_1920x1080p_6000 }


    # S3 Default Input Map.
    # TODO: Get this from unit
    S3_DEFAULT_INPUT_MAP = {
        3: {0: {"card_type": 1, "frame_connector_type": "SDI"},
            1: {"card_type": 1, "frame_connector_type": "SDI"},
            2: {"card_type": 1, "frame_connector_type": "SDI"},
            3: {"card_type": 1, "frame_connector_type": "SDI"},
            },
        4: {0: {"card_type": 2, "frame_connector_type": "DP"},
            1: {"card_type": 2, "frame_connector_type": "DP"},
            2: {"card_type": 2, "frame_connector_type": "HDMI"},
            3: {"card_type": 2, "frame_connector_type": "HDMI"},
            },
        5: {0: {"card_type": 2, "frame_connector_type": "DP"},
            1: {"card_type": 2, "frame_connector_type": "DP"},
            2: {"card_type": 2, "frame_connector_type": "HDMI"},
            3: {"card_type": 2, "frame_connector_type": "HDMI"},
            }
    }

    def __init__(self, parent, frame_str, state_dict={}):
        """Create a new Frame Instance

        Keyword arguments:
        frame_str -- Unique Frame MAC address
        state_dict -- Optional, a dict of Layer state items as defined below

        Frame state items:
        FrameType, BlackOnInvalid
        """
        super(EventMasterFrame, self).__init__(parent)

        if(frame_str == -1):
            # TODO: Should fail here
            return

        self.frame = frame_str

        if state_dict: self.state = state_dict

        self.xml_path_list = ["FrameCollection id='0'",
                              "Frame id='{0!s}'".format(self.frame)]

        return

    def getFrameType(self):
        """(int) Gets Frame Type (E2 or S3)"""
        return self._simple_get("FrameType")

    def setEDIDAsString(self, slot_int, connector_int, edid_string):
        """Sets EDID for a given slot & connector by EDID String

        Keyword arguments:
        (int)slot_int -- Slot number to set EDID on.
                         On an S3, this will be 4-6
                         On an E2, this will be 3-10

        (int)connector_int -- Connector number to set EDID on.

        (str)edid_string -- Formatted EDID string
                            for example: "1920x1080p@50"

        Returns a unique request ID as string
        """
        if slot_int is None or type(slot_int) != int:
            return None

        if connector_int is None or type(connector_int) != int:
            return None

        if edid_string is None or edid_string not in self.STR_MAP:
            return None

        slot_int = int(slot_int)
        connector_int = int(connector_int)
        card_params = self.S3_DEFAULT_INPUT_MAP[slot_int][connector_int]
        edid_params = self.VF_MAP[edid_string]

        if(card_params["frame_connector_type"] == "SDI"):
            return None

        edid_xml = "<VideoFormat id='0'><VFEnum>{11!s}</VFEnum></VideoFormat>"

        edid_type_node_in = ("<{0!s}In id='0'>"
                             "").format(card_params["frame_connector_type"])
        edid_type_node_out = ("</{0!s}In>"
                              "").format(card_params["frame_connector_type"])

        xml_string = ("<Slot id='{0!s}'><Card id='0'><CardIn id='0'>"
                      "<In id='{1!s}'>{2!s}<EDIDIn id='0'>{3!s}</EDIDIn>"
                      "{4!s}</In></CardIn></Card></Slot>"
                      "").format(card_params["slot_index"],
                                 card_params["conn_index"],
                                 edid_type_node_in,
                                 edid_xml,
                                 edid_type_node_out)

        return self.send(xml_string)


class EventMasterCommsXML(EventMasterBase):

    readlock = 0

    def __init__(self, parent, ip, port):
        """Initialise Comms over XML"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.readlock = 0
        self.ip = ip
        self.port = port
        self.parent = parent
        return

    def __gen_guid(self):
        """Generate a UUID to use as unique request identifier"""
        return str(uuid4())

    def close(self):
        """Close Comms over XML"""
        self.socket.close()
        return 1

    def connect(self):
        """Connect over XML"""
        address = (self.ip, self.port)
        try:
            self.socket.connect(address)
        except:
            return 0
        return 1

    def write(self, xml_string, reset=None):
        """Write an XML string

        Keyword arguments:
        xml_string -- XML-formatted string to send,
                      inside System namespace

        Returns a unique request ID as string
        """

        guid_string = self.__gen_guid()

        if reset == "yes":
            xml_ext_string = ("<System id='0' reset='yes' GUID='{0!s}'>"
                              "{1!s}</System>\r\n").format(guid_string,
                                                           xml_string)
        else:
            xml_ext_string = ("<System id='0' GUID='{0!s}'>"
                              "{1!s}</System>\r\n").format(guid_string,
                                                           xml_string)

        self.socket.sendall(xml_ext_string.encode("UTF-8"))
        return guid_string

    def read_next(self):
        """(ElementTree) Read Next Message over XML"""
        if(self.readlock == 1):
            return 0
        else:
            self.readlock = 1

        f = self.socket.makefile("rb")
        c = ""
        newc = ""
        while True:
            newc = f.read(1).decode("utf-8")
            c = "{0!s}{1!s}".format(c, newc)
            if c[-9:] == "</System>":
                break

        self.readlock = 0
        return c


class EventMasterCommsDiscovery(EventMasterBase):

    readlock = 0

    def __init__(self, parent):
        """Initialise Barco Discovery Protocol"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.readlock = 0
        self.parent = parent
        self.discovered = {}
        self._discover()
        return

    def _discover(self):
        """Send Discovery Message to Barco EM Compatible Devices"""
        self.socket.sendto("?\0".encode('UTF-8'), ('255.255.255.255', 40961))
        Timer(0.1, self._recieve_discovery).start()
        return 1

    def _recieve_discovery(self):
        """Loop to recieve and process incoming discovery messages"""
        while True:
            data, addr = self.socket.recvfrom(1024)
            if(data):
                data = data.decode('UTF-8')
                discovered_list = {}
                rtn_list = {}
                x = data.split("\0")
                for item in x:
                    if "=" in item:
                        key, value = item.split("=")
                        discovered_list[key] = value

                if("hostname" in discovered_list):
                    rtn_list['Name'] = discovered_list["hostname"].split(":")[0]
                    rtn_list['Port'] = discovered_list["hostname"].split(":")[1]
                    rtn_list['SystemName'] = discovered_list["hostname"].split(":")[2]
                    rtn_list['MACAddress'] = discovered_list["hostname"].split(":")[5]
                    rtn_list['OSVersion'] = discovered_list["hostname"].split(":")[6]

                if("type" in discovered_list):
                    rtn_list['Type'] = discovered_list['type']

                number_of_items = 0
                rtn_list['IP'] = addr[0]
                for key, value in self.discovered.items():
                    number_of_items += 1
                    if value['IP'] == rtn_list['IP']:
                        self.discovered[key] = rtn_list
                        return 1

                self.discovered[number_of_items] = rtn_list
                return 1

    def getDiscovery(self):
        """Get a dict of currently discovered Barco EM Compatible Devices"""
        return self.discovered


class EventMasterConfigParser(EventMasterBase):

    def __init__(self, parent):
        self.parent = parent
        self.query_status = {}
        return

    def __quick_parse_xml(self, xml_et, key_str, type_str):

        for elem in xml_et.iterfind(key_str):
            if(type_str == "int"):
                return int(elem.text)
            if(type_str == "str"):
                return str(elem.text)

    def parse(self, xml):
        """ Parse XML Config """
        data_et = ET.ElementTree(ET.fromstring(xml))
        data = data_et.getroot()

        parsers = { "FrameCollection": self.__update_framecollection,
                     "SrcMgr/InputCfgCol": self.__update_inputcfgcol,
                     "DestMgr/ScreenDestCol": self.__update_screendestcol,
                     "OutCfgMgr": self.__update_outcfgmgr,
                     "PresetMgr": self.__update_presetmgr  }

        for key,val in parsers.items():
            if data.iterfind(key):
                for iter_et in data.iterfind(key):
                    val(iter_et)

        for resp in data.iterfind("Resp"):
            if resp.text:
                if int(resp.text) == 0:
                    if "GUID" in data.attrib:
                        self.query_status[data.attrib["GUID"]] = 0

        for guiid in data.iterfind("GuiId"):
            if guiid.text:
                self.query_status[guiid.text] = 1

    def getQueryStatus(self, guid_string):
        if guid_string in self.query_status:
            if self.query_status[guid_string] == 0:
                return 0
            else:
                return 1
        else:
            return None

    def __update_inputcfgcol(self, inputcfgcol_et):
        """ Add Node """
        for add_et in inputcfgcol_et.iterfind("Add"):
            if add_et:
                for inputcfg_et in add.iterfind("InputCfg"):
                    self.__update_inputcfg(inputcfg_et)

        """ Remove Node """
        for remove_et in inputcfgcol_et.iterfind("Remove"):
            if remove_et:
                for inputcfg_et in remove.iterfind("InputCfg"):
                    input_id = int(inputcfg_et.attrib["id"])
                    self.parent.inputs.pop(input_id, None)

        """ Update """
        for inputcfg_et in inputcfgcol_et.iterfind("InputCfg"):
            self.__update_inputcfg(inputcfg_et)


    def __update_inputcfg(self, inputcfg_et):
        state_dict = {}
        state_dict["ConnMap"] = []

        if inputcfg_et is None:
            return None

        """ Input ID Attribute necessary """
        if "id" not in inputcfg_et.attrib:
            return None
        input_int = int(inputcfg_et.attrib["id"])

        """ Parse Connector Mapping """
        for connmap_et in inputcfg_et.iterfind("Config/ConnMap"):
            for inuse_et in connmap_et.iterfind("InUse"):

                if(inuse_et.text == "1"):
                    for slotindex_et in connmap_et.iterfind("SlotIndex"):
                        slot_id = int(slotindex_et.text)

                    for connectorindex_et in connmap_et.iterfind("ConnectorIndex"):
                        connector_id = int(connectorindex_et.text)

                    state_dict["ConnMap"].append({"slot":slot_id,"connector:":connector_id})

        """ If no ConnMap attributes, remove from state dict
            (ie. an update with no ConnMap changes) """
        if not state_dict["ConnMap"]:
            state_dict.pop("ConnMap", None)


        """ Parse a number of known items into the state dict"""
        quick_parse_dict = { "FrzMode": "int",
                             "Name": "str",
                             "InputCfgType": "int",
                             "AutoAcqMode": "int",
                             "Type3G": "int" }

        for key,val in quick_parse_dict.items():
            state_dict[key] = self.__quick_parse_xml( inputcfg_et,
                                                          key,
                                                          val)


        """ If input already exists, update state only """
        if input_int in self.parent.inputs:
            self.parent.inputs[input_int].update_state(inputcfg_state)

        else:
            input_obj = EventMasterInput(self.parent,
                                  input_int=int(input_int),
                                  state_dict=state_dict)

            self.parent.inputs[input_int] = input_obj

        return 1


    def __update_framecollection(self, framecollection_et):

        for frame_et in framecollection_et.iterfind("Frame"):
            self.__update_frame(frame_et)


    def __update_frame(self, frame_et):

        state_dict = {}

        if frame_et is None:
            return None

        """ Frame ID Attribute necessary """
        if "id" not in frame_et.attrib:
            return None
        frame_str = str(frame_et.attrib["id"])

        """ Parse a number of known items into the state dict"""
        quick_parse_dict = { "FrameType": "int" }

        for key,val in quick_parse_dict.items():
            state_dict[key] = self.__quick_parse_xml( frame_et, key, val)

        """ If frame already exists, update state only """
        if frame_str in self.parent.frames:
            self.parent.frames[frame_str].update_state(state_dict)

        else:
            frame_obj = EventMasterFrame(self.parent,
                                      frame_str=frame_str,
                                      state_dict=state_dict)

            self.parent.frames[frame_str] = frame_obj

        return 1


    def __update_screendestcol(self, screendestcol_et):
        """ Add Node """
        for add_et in screendestcol_et.iterfind("Add"):
            if add_et:
                for screendest_et in add.iterfind("ScreenDest"):
                    self.__update_screendest(screendest_et)

        """ Remove Node """
        for remove_et in screendestcol_et.iterfind("Remove"):
            if remove_et:
                for screendest_et in remove.iterfind("ScreenDest"):
                    destination_id = int(screendest_et.attrib["id"])
                    self.parent.screendests.pop(destination_id, None)

        """ Update """
        for screendest_et in screendestcol_et.iterfind("ScreenDest"):
            self.__update_screendest(screendest_et)



    def __update_screendest(self, screendest_et):

        state_dict = {}

        if screendest_et is None:
            return None

        """ Destination ID Attribute necessary """
        if "id" not in screendest_et.attrib:
            return None
        destination_int = int(screendest_et.attrib["id"])

        """ Parse a number of known items into the state dict"""
        quick_parse_dict = { "Name": "str",
                             "HSize": "int",
                             "VSize": "int" }

        for key,val in quick_parse_dict.items():
            state_dict[key] = self.__quick_parse_xml( screendest_et, key, val)


        """ If frame already exists, update state only """
        if destination_int in self.parent.screendests:
            self.parent.screendests[destination_int].update_state(state_dict)

        else:
            screendest_obj = EventMasterScreenDestination(self.parent,
                                      destination_int=destination_int,
                                      state_dict=state_dict)

            self.parent.screendests[destination_int] = screendest_obj

        for layer_et in screendest_et.iterfind("LayerCollection/Layer"):
            self.__update_layer(layer_et, destination_int)

        return 1


    def __update_layer(self, layer_et, destination_int):

        state_dict = {}

        if layer_et is None:
            return None

        if destination_int is None or destination_int not in self.parent.screendests:
            return None

        """ Layer ID Attribute necessary """
        if "id" not in layer_et.attrib:
            return None
        layer_int = int(layer_et.attrib["id"])

        xml_owin_prefix = "LayerCfg/LayerState[0]/WinAdjust/OWIN/"

        owin_nodes = { xml_owin_prefix + "VPos": "OWIN_VPos",
                       xml_owin_prefix + "HPos": "OWIN_HPos",
                       xml_owin_prefix + "VSize": "OWIN_VSize",
                       xml_owin_prefix + "HSize": "OWIN_HSize" }

        for key, val in owin_nodes.items():
            for elem in layer_et.iterfind(key):
                state_dict[val] = elem.text

        """ Check for SrcType """
        for elem in layer_et.iterfind("LayerCfg/Source[0]/SrcType"):
            src_type = int(elem.text)
            state_dict["SrcType"] = src_type

        """ SrcType = 0 is Input Source """
        for elem in layer_et.iterfind("LayerCfg/Source[0]/InputCfgIndex"):
            input_id = int(elem.text)
            state_dict["Source"] = input_id

        """ Parse a number of known items into the state dict"""
        quick_parse_dict = { "Name": "str",
                             "PvwMode": "int",
                             "PgmMode": "int",
                             "FrzMode": "int" }

        for key,val in quick_parse_dict.items():
            state_dict[key] = self.__quick_parse_xml( layer_et, key, val)

        self.parent.screendests[destination_int]._updateLayer(layer_int, state_dict)

        return 1


    def __update_outcfgmgr(self, outcfgmgr_et):
        """ Add Node """
        for add_et in outcfgmgr_et.iterfind("Add"):
            if add_et:
                for outputcfg_et in add.iterfind("OutputCfg"):
                    self.__update_outputcfg(outputcfg_et)

        """ Remove Node """
        for remove_et in outcfgmgr_et.iterfind("Remove"):
            if remove_et:
                for outputcfg_et in remove.iterfind("OutputCfg"):
                    output_id = int(outputcfg_et.attrib["id"])
                    self.parent.outputs.pop(output_id, None)

        """ Update """
        for outputcfg_et in outcfgmgr_et.iterfind("OutputCfg"):
            self.__update_outputcfg(outputcfg_et)



    def __update_outputcfg(self, outputcfg_et):

        state_dict = {}

        if outputcfg_et is None:
            return None

        """ Output ID Attribute necessary """
        if "id" not in outputcfg_et.attrib:
            return None
        output_int = int(outputcfg_et.attrib["id"])

        """ Parse a number of known items into the state dict"""
        quick_parse_dict = { "Name": "str" }

        for key,val in quick_parse_dict.items():
            state_dict[key] = self.__quick_parse_xml( outputcfg_et, key, val)

        xml_owin_prefix = "OutputAOI/TestPattern"

        owin_nodes = { xml_owin_prefix + "TestPatternMode": "TestPattern_Mode",
                       xml_owin_prefix + "DiagMotion": "TestPattern_DiagMotion",
                       xml_owin_prefix + "RasterBox": "TestPattern_RasterBox" }

        for key, val in owin_nodes.items():
            for elem in outputcfg_et.iterfind(key):
                state_dict[val] = elem.text

        """ If output already exists, update state only """
        if output_int in self.parent.outputs:
            self.parent.outputs[output_int].update_state(state_dict)

        else:
            output_obj = EventMasterOutput(self.parent,
                                      output_int=output_int,
                                      state_dict=state_dict)

            self.parent.outputs[output_int] = output_obj

        return 1

    def __update_presetmgr(self, presetmgr_et):
        """ Add Node """
        for add_et in presetmgr_et.iterfind("Add"):
            if add_et:
                for preset_et in add.iterfind("Preset"):
                    self.__update_preset(preset_et)

        """ Remove Node """
        for remove_et in presetmgr_et.iterfind("Remove"):
            if remove_et:
                for preset_et in remove.iterfind("Preset"):
                    preset_id = int(preset_et.attrib["id"])
                    self.parent.presets.pop(preset_id, None)

        """ Update """
        for preset_et in presetmgr_et.iterfind("Preset"):
            self.__update_preset(preset_et)


    def __update_preset(self, preset_et):

        state_dict = {}

        if preset_et is None:
            return None

        """ Preset ID Attribute necessary """
        if "id" not in preset_et.attrib:
            return None
        preset_int = int(preset_et.attrib["id"])

        """ Parse a number of known items into the state dict"""
        quick_parse_dict = { "Name": "str" }

        for key,val in quick_parse_dict.items():
            state_dict[key] = self.__quick_parse_xml( preset_et, key, val)

        """ If preset already exists, update state only """
        if preset_int in self.parent.presets:
            self.parent.presets[preset_int].update_state(state_dict)

        else:
            preset_obj = EventMasterPreset(self.parent,
                                      preset_int=preset_int,
                                      state_dict=state_dict)

            self.parent.presets[preset_int] = preset_obj

        return 1


class EventMasterSwitcher(EventMasterBase):

    QUERY_HANDSHAKE = ("<XMLType>3</XMLType><Query>3</Query>"
                       "<Recursive>1</Recursive>")

    # TODO: Get this from the device config
    VALID_REFRESH_RATES = {"23.98", "24", "25", "29.97", "30", "47.95", "48",
                           "50", "59.94", "60"}

    S3_DEFAULT_REV_INPUT_MAP = {3: {0: 1, 1: 2, 2: 3, 3: 4},
                                4: {0: 5, 1: 6, 2: 7, 3: 8},
                                5: {0: 9, 1: 10, 2: 11, 3: 12}}

    def __init__(self):
        """Initialise new Switcher instance"""
        self.sys = {"port": 9876, "ip": u"127.0.0.1"}
        self.verbose = 1
        self.connected = self.ready = 0
        self.inputs = {}
        self.screendests = {}
        self.frames = {}
        self.outputs = {}
        self.presets = {}
        self.recieved_guids = {}
        self.CommsDiscovery = EventMasterCommsDiscovery(self)
        self.ConfigParser = EventMasterConfigParser(self)
        self.updateThread = Thread(target=self.__update)
        self.updateThread.daemon = True
        self.updateThread.start()
        return None

    def __do_handshake(self):
        """Switcher do_handshake()"""
        return self.send(self.QUERY_HANDSHAKE, reset="yes")

    def start(self):
        """Switcher start()"""
        self.ready = 2


        if(self.connected):
            self.ready = 0
            return None

        if "ip" not in self.sys:
            self.ready = 0
            return None

        self.CommsXML = EventMasterCommsXML(self, self.sys["ip"], 9876)

        if not self.CommsXML.connect():
            self.ready = 0
            return None

        self.__do_handshake()
        self.connected = 1
        return True

    def stop(self):
        """Switcher stop()"""

        if not self.CommsXML.close():
            return None

        self.connected = 0
        self.ready = 0
        return True

    def loadFromXML(self, xml_string):
        if xml_string is None:
            return None
        else:
            self.ConfigParser.parse(xml_string)

    def send(self, data):
        return self.CommsXML.write(data)

    def __update(self):
        """Switcher __update() loop"""
        while(1):
            if(self.connected == 1):
                try:
                    data = self.CommsXML.read_next()
                    self.ConfigParser.parse(data)
                    self.ready = 1
                except Exception, e:
                    pass

                if data is None:
                    pass

            else:
                sleep(1)

        return None

    def getDiscovery(self):
        return self.CommsDiscovery.getDiscovery()

    def cmdSend(self, data):
        return self.CommsXML.write(data)

    def getQueryStatus(self, guid_string):
        return self.ConfigParser.getQueryStatus(guid_string)

    def setVerbose(self, verbose_bool):
        """Switcher set_verbose()"""
        if not verbose_bool and type(verbose_bool) != bool:
            return None

        self.verbose = int(verbose_bool)
        return 1

    def getVerbose(self):
        """Switcher get_verbose()"""
        if not hasattr(self, "verbose"):
            return -1

        return int(self.verbose)

    def setIP(self, ip_string):
        """Switcher set_CommsXML_IP()"""
        if not ip_string and type(ip_string) != str:
            return None

        self.sys["ip"] = str(ip_string)
        return 1

    def getIP(self):
        """Switcher get_CommsXML_IP()"""
        if not hasattr(self.sys, "ip"):
            return -1

        return str(self.sys["ip"])

    def isReady(self):
        """Switcher is_ready()"""
        if not hasattr(self, "ready"):
            return None
        return int(self.ready)

    def getInputs(self):
        """Switcher enum_inputs()"""
        if not self.inputs:
            return {}

        inputs_list = {}

        for key, inst in self.inputs.items():
            inputs_list[key] = inst

        return inputs_list

    def getScreenDests(self):
        if not self.screendests:
            return {}

        screendests_list = {}

        for key, inst in self.screendests.items():
            screendests_list[key] = inst

        return screendests_list

    def getFrames(self):
        if not self.frames:
            return {}

        frames_list = {}

        for key, inst in self.frames.items():
            frames_list[key] = inst

        return frames_list

    def getOutputs(self):
        if not self.outputs:
            return {}

        return self.outputs

    def getPresets(self):
        if not self.presets:
            return {}

        return self.presets

    def setNativeRate(self, rate_hz):
        """Switcher set_NativeRate"""
        if rate_hz not in self.VALID_REFRESH_RATES:
            return -1

        xml = "<NativeRate>{$0!s}</NativeRate>".format(rate_hz)
        return self.send(xml)

    def setName(self, name):
        """Switcher set_Name()"""
        if not name:
            return -1

        xml = "<Name>{$0!s}</Name>"
        return self.send(xml)

    def cmdCut(self):
        """Switcher cmd_Cut()"""
        xml = "<PresetMgr><Cut></Cut></PresetMgr>"
        return self.send(xml)

    def cmdAutoTrans(self):
        """Switcher cmd_AutoTrans()"""
        xml = "<PresetMgr><AutoTrans></AutoTrans></PresetMgr>"
        return self.send(xml)

    def cmdSavePreset(self, preset_id):
        if preset_id is None:
            return None

        xml = "<PresetMgr><SavePreset>{0!s}</SavePreset></PresetMgr>".format(preset_id)
        return self.send(xml)
