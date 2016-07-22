# coding: utf-8
## @package FaBoRTC_PCF2129
#  This is a library for the FaBo Ambient Light I2C Brick.
#
#  http://fabo.io/217.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import smbus
import time

SLAVE_ADDRESS = 0x44 # ISL29034 I2C Slave Address
DEVICE_ID     = 0x28 # ISL29034 Device ID(xx101xxx)

# Register Addresses
REG_CMD1    = 0x00
REG_CMD2    = 0x01
REG_DATA_L  = 0x02
REG_DATA_H  = 0x03
REG_ID      = 0x0F

# Operation Mode
OP_PWR_DOWN = 0x00 # Power-down the device(Default)
OP_ALS_CONT = 0xA0 # Measures ALS continuously

# FULL SCALE LUX RANGE
FS_0    = 0x00 # 1,000(Default)
FS_1    = 0x01 # 4,000
FS_2    = 0x02 # 16,000
FS_3    = 0x03 # 64,000

# ADC RESOLUTION
RES_16  = 0x00 # 16bit(Default)
RES_12  = 0x04 # 12bit
RES_8   = 0x08 # 8bit
RES_4   = 0x0C # 4bit

ID_MASK = 0x38 # ISL29034 Device ID Mask(00111000)

## smbus
bus = smbus.SMBus(1)

##  FaBo Ambient Light I2C Controll class
class ISL29034:

    ## Constructor
    #  @param [in] address PCF2129 i2c slave_address default:0x44
    def __init__(self, address=SLAVE_ADDRESS):
        self.address    = address
        self.range      = FS_0
        self.resolution = RES_16

        self.setOperation(OP_ALS_CONT)
        self.setRange(FS_3)
        self.setResolution(RES_16)

    ## Search Device
    #  @retval true  device connected
    #  @retval false device error
    def searchDevice(self):
        data = bus.read_byte_data(self.address, REG_ID)
        if (data & ID_MASK) == DEVICE_ID:
            return True
        else:
            return False

    ## Set Operation Mode
    #  @param [in] config Operation Mode DEFAULT:Power-down the device
    def setOperation(self, config = OP_PWR_DOWN):
        bus.write_byte_data(self.address, REG_CMD1, config)

    ## Set FullScale Range
    #  @param [in] config FullScale Range DEFAULT:FULL SCALE LUX RANGE 1,000
    def setRange(self, config = FS_0):
        self.range = config
        data = bus.read_byte_data(self.address, REG_CMD2)

        data &= 0xFC  # 11111100
        data |= config

        bus.write_byte_data(self.address, REG_CMD2, data)

    ## Set ADC Resolution
    #  @param [in] config Resolution DEFAULT:ADC RESOLUTION 16Bit
    def setResolution(self, config = RES_16):
        self.resolution = config
        data = bus.read_byte_data(self.address, REG_CMD2)

        data &= 0xF3  # 11110011
        data |= config

        bus.write_byte_data(self.address, REG_CMD2, data)

    ## Read ADC data
    #  @return ADC data
    def readADC(self):

        if self.resolution == RES_16:
            time.sleep(0.09)
        elif self.resolution == RES_12:
            time.sleep(0.006)
        elif self.resolution == RES_8:
            time.sleep(0.000352)
        elif self.resolution == RES_4:
            time.sleep(0.000022)

        data = bus.read_i2c_block_data(self.address, REG_DATA_L, 2)
        adc = (data[1]<<8) | data[0]
        return adc

    ## Read lux data
    #  @return lux data
    def read(self):
        adc = self.readADC()

        if self.range == FS_0:
            range = 1000
        elif self.range == FS_1:
            range = 4000
        elif self.range == FS_2:
            range = 16000
        elif self.range == FS_3:
            range = 64000

        if self.resolution == RES_16:
            count = 65535
        elif self.resolution == RES_12:
            count = 4095
        elif self.resolution == RES_8:
            count = 255
        elif self.resolution == RES_4:
            count = 15

        return float(range) / count * adc
