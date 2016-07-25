# coding: utf-8
## @package FaBoBLE_BLE113
#  This is a library for the FaBo BLE113 Brick.
#
#  http://fabo.io/301.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import serial
import time

# Wait time before BGAPI response.
WAIT_REPLY = 0.5

## Scan Data Buffer size
BUFF_SIZE = 11

## Beacon Data Max size
DATA_LEN  = 31

## BLE113 Control Class
class BLE113:
    rssi       = [0 for i in range(BUFF_SIZE+1)]
    packettype = [0 for i in range(BUFF_SIZE+1)]
    sender     = [[0 for i in range(6)] for j in range(BUFF_SIZE+1)]
    addrtype   = [0 for i in range(BUFF_SIZE+1)]
    bond       = [0 for i in range(BUFF_SIZE+1)]
    data_len   = [0 for i in range(BUFF_SIZE+1)]
    data       = [[0 for i in range(DATA_LEN)] for j in range(BUFF_SIZE+1)]

    ## Command(Set Adv Data).
    # Set advertisement or scan response data.
    # The custom data is only used when the discoverable mode is set to gap_user_data.
    # V.1.3 API DOCUMENTATION Version 3.2 P95
    COMMAND_SEND_BEACON = [
        0x00, # message type, 0x00:command.
        0x20, # Minimum payload length, 0x20=32 bytes.
        0x06, # Message class, 0x06:Generic Access Profile.
        0x09, # Message ID, 0x09.
        0x00, # Advertisement data type, 0x00: sets advertisement data.
        0x1e  # Advertisement data to send.
    ]
    ## Command(Set Mode).
    #  Configures the current GAP discoverability and connectability mode.
    #  It is used to turn the module into a Slave by starting advertisement in connectable mode
    #  V.1.3 API DOCUMENTATION Version 3.2 P101
    COMMAND_SET_MODE_FOR_BEACON = [
        0x00, # message type, 0x00:command
        0x02, # Minimum payload length
        0x06, # Message class, 0x06:Generic Access Profile
        0x01, # Message ID, 0x01
        0x04, # GAP Discoverable Mode
        0x00  # GAP Connectable Mode
    ]

    ## Command(Set Adv Parameters).
    #  Sets the advertising parameters.
    #  V.1.3 API DOCUMENTATION Version 3.2 P96.
    COMMAND_SET_ADV_PARAMETERS_FOR_BEACON = [
        0x00, # Message type -> 0x00:command.
        0x05, # Minimum payload length -> 0x05:5 Bytes.
        0x06, # Message class -> 0x06:Generic Access Profile.
        0x08, # Message ID -> 0x08.
        0x00, # Minimum advertisement[0].
        0x02, # Minimum advertisement[1].
        0x00, # Maximum advertisement[0].
        0x02, # Maximum advertisement[1].
        0x07  #  Advertisement channels, 0x07: All three channels are used
    ]

    ## Command(Set Mode).
    #  Configures the current GAP discoverability and connectability mode.
    #  It is used to turn the module into a Slave by starting advertisement in connectable mode
    #  V.1.3 API DOCUMENTATION Version 3.2 P101
    COMMAND_STOP_MODE_STOP_FOR_BEACON = [
        0x00, # message type  -> 0x00:command.
        0x02, # Minimum payload length -> 0x02:2 Bytes.
        0x06, # Message class -> 0x06:Generic Access Profile.
        0x01, # Message ID -> 0x01.
        0x00, # GAP Discoverable Mode -> 0x00:gap_non_discoverable.
        0x00  # GAP Connectable Mode.
    ]

    ## Command(Discover).
    #  Resets the local device immediately.
    #  The command does not have a response.
    #  V.1.3 API DOCUMENTATION Version 3.2 P93
    COMMAND_START_DISCOVER = [
        0x00, # message type  -> 0x00:command.
        0x01, # Minimum payload length -> 0x01:1 Bytes.
        0x06, # Message class -> 0x06:GAP.
        0x02, # Message ID -> 0x02.
        0x01  # mode -> 0x01:gap_discover_generic.
    ]

    # Command(Reset).
    # Resets the local device immediately.
    # The command does not have a response.
    # V.1.3 API DOCUMENTATION Version 3.2 P181
    COMMAND_RESET = [
        0x00, # message type  -> 0x00:command.
        0x01, # Minimum payload length -> 0x01:1 Bytes.
        0x00, # Message class -> 0x00:System.
        0x00, # Message ID -> 0x01.
        0x00  # Selects the boot mode -> 0x00:boot to main program
    ]

    pos = 0        # 現在の設定位置
    dataCount = 0  # 取得しているレコード件数
    scanLen = 1    #
    dataIn = 0     # レコード書き込み位置
    dataOut = 0    # レコード読み込み位置
    broken = False # データ破損判定

    # count of buffer.
    buffCount = 0

    # flag of Debug.
    DEBUG = False

    #! status of advertising.
    is_advertising = False

    #! status of scanning.
    is_scanning = False

    ## init.
    #  @param [in] serialport BLE port
    #  @param [in] rate       Baud rate
    def __init__(self, serialport, rate):
        # Serial Open
        self.bleBrick = serial.Serial(serialport, rate, timeout=1)
        # send BGAPI command
        self.sendCommand(self.COMMAND_RESET)
        # Wait reply.
        time.sleep(WAIT_REPLY)

        # Flash of software serial.
        while self.bleBrick.inWaiting()>0 :
            buffer = self.bleBrick.readline()

    ## Enable debug message.
    def setDebug(self):
        self.DEBUG = True

    ## Set beacon uuid.
    #  @param [in] uuid[] UUID(16bytes)
    def setBeaconUuid(self, uuid):
        self.uuid=uuid

    ## Set beacon major id.
    #  @param [in] major[] majorId(2bytes)
    def setBeaconMajor(self, major):
        self.major=major

    ## Set beacon minor id.
    #  @param [in] major[] minorId(2bytes)
    def setBeaconMinor(self, minor):
        self.minor=minor

    ## send beacon(start advertising).
    def sendBeacon(self):

        # send BGAPI command.
        self.sendCommand(self.COMMAND_SEND_BEACON)

        # iBeacon header.
        beaconHeader= [
            0x02, # Flags[0], Bluetooth 4.0 Core Specification
            0x01, # Flags[1], Bluetooth 4.0 Core Specification
            0x06, # Flags[2], Bluetooth 4.0 Core Specification
            0x1A, # Length, Bluetooth 4.0 Core Specification
            0xFF, # Type, Bluetooth 4.0 Core Specification
            0x4C, # Company ID[0]
            0x00, # Company ID[1]
            0x02, # Beacon Type[0]
            0x15  # Beacon Type[1]
        ]

        # send iBeacon header.
        for header in beaconHeader:
            self.bleBrick.write(chr(header))

        # send iBeacon UUID.
        for uuid in self.uuid:
            self.bleBrick.write(chr(uuid))

        # send iBeacon MajorID.
        for major in self.major:
            self.bleBrick.write(chr(major))

        # send iBeacon MinorID.
        for minor in self.minor:
            self.bleBrick.write(chr(minor))

        # send txPower.
        self.bleBrick.write(chr(0xC9))

        # Waiting reply.
        time.sleep(WAIT_REPLY)

        # Receive reply.
        buffer = self.bleBrick.readline()

        if(self.errorCheck(buffer)):
            return True
        else:
            return False

    ## set mode.
    def setMode(self):
        # send BGAPI command.
        self.sendCommand(self.COMMAND_SET_MODE_FOR_BEACON)

        # Waiting reply.
        time.sleep(WAIT_REPLY)

        # recieve BGAPI response.
        buffer = self.bleBrick.readline()
        if self.errorCheck(buffer):
            self.is_advertising = True
            return True
        else:
            return False
    ## Set Adv Parameters.
    def setAdvParameters(self):
        # send BGAPI command.
        self.sendCommand(self.COMMAND_SET_ADV_PARAMETERS_FOR_BEACON)

        # Waiting reply.
        time.sleep(WAIT_REPLY)

        # Receive BGAPI response.
        buffer = self.bleBrick.readline()

        return self.errorCheck(buffer)

    ## stop advertising.
    def stopAdv(self):
        # send BGAPI command.
        self.sendCommand(self.COMMAND_STOP_MODE_STOP_FOR_BEACON)

        # Waiting reply.
        time.sleep(WAIT_REPLY)

        # Receive BGAPI response.
        buffer = self.bleBrick.readline()

        if(self.errorCheck(buffer)):
            self.is_advertising = False
            return True
        else:
            return False

    ## Scan data analysis
    def tick(self):

        if self.broken == True:
            self.bleBrick.flushInput()

        if self.bleBrick.inWaiting()>0:
            readData = self.bleBrick.read().encode('hex')
            intData = int(readData,16)

            # skip broken data
            if (self.broken):
                return


            if self.pos==0:
                if intData != 0x80:
                    self.broken = True
            elif self.pos==1:
                self.scanLen = intData + 3

                # impossible value is broken data...
                if self.scanLen < 0 or self.scanLen > 50:
                    self.broken = True

            elif self.pos==4:
                self.clearScanData(self.dataIn)

                if intData & (1 << 8 -1):
                    intData -= (1<<8)
                self.rssi[self.dataIn] = intData

            # PacketType
            elif self.pos==5:
                self.packettype[self.dataIn] = intData

            # AddrType
            elif self.pos==12:
                self.addrtype[self.dataIn] = intData

            # Bond
            elif self.pos==13:
                self.bond[self.dataIn] = intData

            # data size
            elif self.pos==14:
                self.data_len[self.dataIn] = intData

            # Sender , data
            else:
                # Sender
                if (5 < self.pos) and (self.pos < 12):
                    self.sender[self.dataIn][self.pos-6] = intData

                elif self.pos > 14:
                    if self.pos - 14 <= DATA_LEN:
                        self.data[self.dataIn][self.pos-14] = intData

            self.pos += 1

            # end of data
            if (self.pos > self.scanLen):
                self.pos = 0
                self.scanLen = 1
                self.dataCount += 1
                self.dataIn += 1
                self.dataIn %= BUFF_SIZE
                if (self.dataIn == self.dataOut):
                    #Delete old data
                    self.dataOut += 1
                    self.dataCount -= 1
        elif self.broken==True:
            self.pos = 0
            self.scanLen = 1
            self.broken = False

    ## Set scan parameters
    #  @param [in] param set scan parameters
    def setScanParams(self, param):

        self.bleBrick.write(chr(0x00))
        self.bleBrick.write(chr(0x05))
        self.bleBrick.write(chr(0x06)) # class
        self.bleBrick.write(chr(0x07))
        self.bleBrick.write(chr(param[0])) # scan_interval 1  0x00XX  0x4 - 0x0004
        self.bleBrick.write(chr(param[1])) # scan_interval 2  0xXX00
        self.bleBrick.write(chr(param[2])) # scan_window  1  0x00XX
        self.bleBrick.write(chr(param[3])) # scan_window  2  0xXX00
        self.bleBrick.write(chr(param[4]))  # 0x01,

        # Waiting reply.
        time.sleep(WAIT_REPLY)

        # Receive BGAPI response.
        buffer = self.bleBrick.readline()

        return self.errorCheck(buffer)

    ## Scan start.
    def scan(self):

        # send BGAPI command.
        self.sendCommand(self.COMMAND_START_DISCOVER)

        time.sleep(0.1)

        buffer=[]
        i = 0

        # Receive BGAPI response.
        while (self.bleBrick.inWaiting()>0):
            buffer.append(self.bleBrick.read())

            i += 1
            if (i > 5):
                break

        return self.errorCheck(buffer)

    ## Status of advertising.
    def isAdvertising(self):
        return self.is_advertising

    ## Status is scanning.
    def isScanning(self):
        return self.is_scanning

    ## Send command.
    #  @param [in] command send command
    def sendCommand(self, command):
        # send BGAPI command.
        for cmd in command:
            self.bleBrick.write(chr(cmd))

    ## Error check.
    #  @param [in] buffer BLE113 response data
    def errorCheck(self, buffer):

        buf0 = int(buffer[0].encode('hex'))
        buf1 = int(buffer[1].encode('hex'))
        buf2 = int(buffer[2].encode('hex'))

        # Error check.
        if(buf0 == 0x00 and buf1 == 0x02 and buf2 == 0x06):

            buf4 = int(buffer[4].encode('hex'))
            buf5 = int(buffer[5].encode('hex'))

            if(buf4 == 0x00 and buf5 == 0x00):
                return True
            else:
                if(self.DEBUG):
                    print "Error Code",buffer[5].encode('hex'),buffer[4].encode('hex')
                return False
        else:
            if(self.DEBUG):
                print "Unknow Error"
                print buffer[0].encode('hex')
                print buffer[1].encode('hex')
                print buffer[2].encode('hex')
                print buffer[3].encode('hex')
                print buffer[4].encode('hex')
                print buffer[5].encode('hex')
        return False

    ## Clear ScanData
    #  @param [in] point scandata clear point
    def clearScanData(self, point):
        self.rssi[point]       = 0
        self.packettype[point] = 0
        for i in range(6):
            self.sender[point][i]  = 0
        self.addrtype[point]   = 0
        self.bond[point]       = 0
        self.data_len[point]   = 0
        self.data[:][point]    = 0
        for i in range(DATA_LEN):
            self.data[point][i]  = 0

    ## Get ScanData Count.
    def getDataCount(self):
        return self.dataCount

    ## Get ScanData.
    def getScanData(self):
        if (self.dataCount == 0):
            out={
                "rssi"      : 0,
                "packettype": 0,
                "sender"    : 0,
                "addrtype"  : 0,
                "bond"      : 0,
                "data_len"  : 0,
                "data"      : 0
            }
            return out
        out={
            "rssi"      : self.rssi[self.dataOut],
            "packettype": self.packettype[self.dataOut],
            "sender"    : self.sender[self.dataOut][:],
            "addrtype"  : self.addrtype[self.dataOut],
            "bond"      : self.bond[self.dataOut],
            "data_len"  : self.data_len[self.dataOut],
            "data"      : self.data[self.dataOut][:]
        }
        self.dataOut += 1
        self.dataOut %= BUFF_SIZE
        self.dataCount -= 1
        return out
