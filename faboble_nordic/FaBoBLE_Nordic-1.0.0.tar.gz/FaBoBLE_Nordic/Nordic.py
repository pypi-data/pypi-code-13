# coding: utf-8
## @package FaBoBLE_Nordic
#  This is a library for the FaBo Nordic Brick.
#
#  http://fabo.io/307.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import serial
import time
import sys

# Wait time before response.
WAIT_REPLY = 1.5

BUFF_SIZE = 11
DATA_LEN  = 50

class Nordic:
    handle     = [0 for i in range(BUFF_SIZE+1)]
    addrtype   = [0 for i in range(BUFF_SIZE+1)]
    address    = [[0 for i in range(8)] for j in range(BUFF_SIZE+1)]
    rssi       = [0 for i in range(BUFF_SIZE+1)]
    flags      = [0 for i in range(BUFF_SIZE+1)]
    data_len   = [0 for i in range(BUFF_SIZE+1)]
    data       = [[0 for i in range(DATA_LEN)] for j in range(BUFF_SIZE+1)]

    # command data
    c_len      = 0
    c_type     = 0x00
    c_command  = 0x00
    c_data     = [0 for i in xrange(50)]

    pos       = 0     # 現在の設定位置
    dataCount = 0     # 取得しているレコード件数
    scanLen   = 1     #
    dataIn    = 0     # レコード書き込み位置
    dataOut   = 0     # レコード読み込み位置
    broken    = False # データ破損判定
    ofs       = 0


    # count of buffer.
    buffCount = 0

    # flag of Debug.
    DEBUG = False

    #! status of advertising.
    is_advertising = False

    #! status of scanning.
    is_scanning = False

    ## init.
    #  @param [in] serialport port
    #  @param [in] rate       baud rate
    def __init__(self, serialport, rate):
        # Serial Open
        self.bleNordic = serial.Serial(serialport, rate, timeout=1)

        # stopScan
        self.stopScan()
        time.sleep(WAIT_REPLY)
        self.bleNordic.flush()
        
        # setEnable
        self.sd_ble_enable()

        # Wait reply.
        time.sleep(WAIT_REPLY)

        # Flash of software serial.
        while self.bleNordic.inWaiting()>0 :
            buffer = self.bleNordic.readline()

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

    # Beaconデータ設定
    ## Advertise Data Set.
    def setAdvData(self):

        sd_ble_gap_adv_data_set_cmd = 0x72
        # iBeacon header.
        beacon_data= [
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

        txpower = [0xc9]

        beacon_data += self.uuid + self.major + self.minor + txpower

        send_data = [
            len(beacon_data), # data size
            0x01]             # data present

        send_data += beacon_data
        send_data += [0x00, 0x00]

        # adv_data set command.
        self.sendCommand(sd_ble_gap_adv_data_set_cmd, send_data)

        # Waiting reply.
        time.sleep(WAIT_REPLY)

        # Receive reply.
        buffer = self.bleNordic.readline()

        if self.errorCheck(buffer):
            self.is_advertising = True
            return True
        else:
            return False

    ## BLE有効化
    #  @param [in] service_changed default 0
    #  @param [in] attr_tab_size   default 0
    def sd_ble_enable(self, service_changed=0, attr_tab_size=0):
        sd_ble_enable_cmd = 0x60

        data = [
            0x01,
            service_changed,
    	    attr_tab_size >> 8 & 0xff,
            attr_tab_size & 0xff,
            0x00,
            0x00
        ]
        self.sendCommand(sd_ble_enable_cmd, data)

        # Wait reply.
        time.sleep(WAIT_REPLY)

        # response.
        buffer = self.bleNordic.readline()

        return self.errorCheck(buffer)

    ## start Advertise
    def startAdv(self):
        sd_ble_gap_adv_start_cmd = 0x73

        data = [
            0x01,
            0x00, # GAP Advertising Type
            0x00, # Peer Address Present
            0x00, # Filter Policy
            0x00, # GAP Whitelist Present
            0x40, 0x06, # Interval(0.625 ms units)
            0x00, 0x00, # Timeout(No timeout)
            0x00 # Channel Mask
        ]

        self.sendCommand(sd_ble_gap_adv_start_cmd, data)

        # response.
        buffer = self.bleNordic.readline()

        if self.errorCheck(buffer):
            self.is_advertising = True
            return True
        else:
            return False

    ## stop Advertise
    def stopAdv(self):
        sd_ble_gap_adv_stop_cmd = 0x74

        data = []

        self.sendCommand(sd_ble_gap_adv_stop_cmd, data)

        # recieve response.
        buffer = self.bleNordic.readline()

        if self.errorCheck(buffer):
            self.is_advertising = False
            return True
        else:
            return False

    ## start BLE Scan
    def startScan(self):
        sd_ble_gap_scan_start_cmd = 0x86
        data = [
            0x01, # Scan Params field present : present
            0x00, # Active, selective fields
            0x00, # GAP Whitelist field present : not present
            0xa0, 0x00, # Scan interval
            0x50, 0x00, # Scan window
            0x00, 0x00  # time out
        ]
        self.sendCommand(sd_ble_gap_scan_start_cmd, data)

    ## stop BLE Scan
    def stopScan(self):
        sd_ble_gap_scan_stop_cmd = 0x87

        data = []

        self.sendCommand(sd_ble_gap_scan_stop_cmd, data)
        time.sleep(0.5)

    ## スキャンデータ解析
    def tick(self):

        if self.broken == True:
            self.bleNordic.flush()
            print "broken"   

        if self.bleNordic.inWaiting()>0:
              
            readData = self.bleNordic.read().encode('hex')
            intData = int(readData,16)

            # skip broken data
            if (self.broken):
                return
            # データサイズ１
            if self.pos==0:
                self.c_len = intData

            # データサイズ２
            elif self.pos==1:
                self.c_len = self.c_len | (intData << 8)
                # impossible value is broken data...
                if (self.c_len < 2) or (self.c_len > 50):
                    broken = True

            # データタイプ: 0:command 1:response 2:event
            elif self.pos==2:
                self.c_type = intData
                # impossible value is broken data...
                if intData in (1, 3):
                    self.ofs = 2
                elif intData == 2:
                    self.ofs = 3
                else:
                    broken = True

            # コマンド
            elif self.pos==3:
                self.c_command = intData

            # Data
            else:
                if (self.pos - self.ofs - 2) >= 0:
                    self.c_data[self.pos - self.ofs - 2] = intData

            # end of data
            if self.pos > self.c_len :

                self.c_len -= self.ofs
                # end of data
                # データ解析
                self.nrfReceive()
                self.pos        = 0
                self.c_len      = 0
                self.c_type     = 0x00
                self.c_command  = 0x00
                self.c_data     = [0 for i in xrange(50)]

                self.ofs        = 0

            else:
                self.pos += 1

        elif self.broken==True:
            self.pos        = 0
            self.c_len      = 0
            self.c_type     = 0x00
            self.c_command  = 0x00
            self.c_data     = [0 for i in xrange(50)]

            self.ofs        = 0
            self.broken = False

    # nrfデータ解析
    def nrfReceive(self):
        # BLE_GAP_EVT_CONNECTED
        if (self.c_command == 0x10):
            if self.DEBUG:
                print "\n*BLE_GAP_EVT_CONNECTED"
                print "Connection Handle:"
                print self.c_data[0],
                print self.c_data[1]
                print "Peer Address:",
                for i in xrange(7):
                    print self.c_data[2+i],
                print "\nOwn Address:"
                for i in xrange(7):
                    print self.c_data[9+i],
                print "\nIRK:"
                print self.c_data[17]
                print "GAP Connection Parameters:"
                for i in xrange(8):
                    print self.c_data[18+i],
                print

        # BLE_GAP_EVT_DISCONNECTED
        elif self.c_command == 0x11:
            if self.DEBUG:
                print "\n*BLE_GAP_EVT_CONNECTED"
                print "Connection Handle:"
                print self.c_data[0],
                print self.c_data[1],
                print "Reason:"
                print self.c_data[2],
            print

        # BLE_GAP_EVT_ADV_REPORT
        elif self.c_command == 0x1b:
            if self.DEBUG:
                print "\n*BLE_GAP_EVT_ADV_REPORT"
                print "Connection Handle:",
                print self.c_data[0],
                print self.c_data[1]
                print "Address Type:"
                print self.c_data[2]
                print "Address:",
                for i in xrange(6):
                    print self.c_data[3+i]
                print "\nRSSI:"
                print self.c_data[9]
                print "Flags:"
                print self.c_data[10],
                print "DataLen:"
                print self.c_len
                print "Data:"
                for i in xrange(self.c_len-11):
                    print self.c_data[11+i]
                print

            # send event to handler
            self.handle[self.dataIn] = self.c_data[0] |  self.c_data[1] << 8
            self.addrtype[self.dataIn] = self.c_data[2]
            for i in xrange(5, -1, -1):
                self.address[self.dataIn][i] = self.c_data[i + 3]

            value = self.c_data[9]
            # int -> int16
            if value & 0x80:
                value -= (1<<8)
            self.rssi[self.dataIn] = value

            self.flags[self.dataIn] = self.c_data[10]
            self.data_len[self.dataIn] = self.c_len - 11
            for i in xrange(self.data_len[self.dataIn]):
                 self.data[self.dataIn][i] = self.c_data[i + 11]

            self.dataIn += 1
            self.dataIn %= BUFF_SIZE
            self.dataCount += 1
            if self.dataIn == self.dataOut:
                self.dataOut   += 1
                self.dataCount -= 1

        # BLE_SCAN START RESPONSE
        elif self.c_command == 0x86:
            if self.DEBUG:

                print "\n*BLE_SCAN_START RESPONSE"
                print "Error Code:"
                print self.c_data[0], self.c_data[1], self.c_data[2], self.c_data[3]

            check_data = self.c_data[0] | self.c_data[1] | self.c_data[2] | self.c_data[3]

            if check_data == 0:
                print "BLE Scan Start"
                self.is_scanning = True
            else:
                print "BLE Scan Failed"

        # BLE_SCAN STOP RESPONSE
        elif self.c_command == 0x87:
            if self.DEBUG:

                print "\n*BLE_SCAN_STOP RESPONSE"
                print "Error Code:"
                print self.c_data[0], self.c_data[1], self.c_data[2], self.c_data[3]

            check_data = self.c_data[0] | self.c_data[1] | self.c_data[2] | self.c_data[3]

            if check_data == 0:
                print "BLE Scan Stop"
                self.is_scanning = False
            else:
                print "BLE Scan Stop Failed"

    # Status of advertising.
    def isAdvertising(self):
        return self.is_advertising

    ## Status is scanning.
    def isScanning(self):
        return self.is_scanning

    ## Send command.
    #  param [in] command Send Command
    #  param [in] data    Send Data
    def sendCommand(self, command, data):
        # send Data Size
        data_len = len(data)+2

        self.bleNordic.write(chr(data_len & 0xff))      # packet size 2
        self.bleNordic.write(chr((data_len >> 8) & 0xff)) # packet size 1
        self.bleNordic.write(chr(0))                    # type: 0=command
        self.bleNordic.write(chr(command))              # command

        # send command.
        for value in data:
            self.bleNordic.write(chr(value))

    ## Error check.
    #  @param [in] buffer nrf Responce data
    def errorCheck(self, buffer):
        
        i = 0
        for value in buffer:
            if i == 3:
                 cmd= int(value.encode('hex'),16)
            elif i == 4:
                err1 = int(value.encode('hex'),16)
            elif i == 5:
                err2 = int(value.encode('hex'),16)
            elif i == 6:
                err3 = int(value.encode('hex'),16)
            elif i == 7:
                err4 = int(value.encode('hex'),16)

            i += 1

        # Error check.
        if (err1 | err2 | err3 | err4) == 0:
            return True

        else:
            if(self.DEBUG):
                print "Response Error"
                print "Command:", hex(cmd)
                print " ERROR CODE:", hex(err1), hex(err2), hex(err3), hex(err4) 
            return False

    ## Clear ScanData
    #  @param [in] point ScanData Clear point
    def clearScanData(self, point):
        self.rssi[point] = 0
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

    # Get ScanData.
    def getScanData(self):
        if (self.dataCount == 0):
            out={
                "handle"    : 0,
                "addrtype"  : 0,
                "address"   : 0,
                "rssi"      : 0,
                "data_len"  : 0,
                "data"      : 0
            }
            return out

        out={
            "handle"    : self.handle[self.dataOut],
            "addrtype"  : self.addrtype[self.dataOut],
            "address"   : self.address[self.dataOut][:],
            "rssi"      : self.rssi[self.dataOut],
            "data_len"  : self.data_len[self.dataOut],
            "data"      : self.data[self.dataOut][:]
        }
        self.dataOut += 1
        self.dataOut %= BUFF_SIZE
        self.dataCount -= 1
        return out

