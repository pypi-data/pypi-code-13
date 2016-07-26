# coding: utf-8
## @package FaBoProximity_VCNL4010
#  This is a library for the FaBo Proximity I2C Brick.
#
#  http://fabo.io/205.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import smbus
import time

## I2C VCNL4010 Slave Address
SLAVE_ADDRESS = 0x13

## Product,Revision ID Value
DEVICE_ID     = 0x21

# Register Addresses
REG_CMD         = 0x80
REG_ID          = 0x81
REG_PROX_RATE   = 0x82
REG_LED_CRNT    = 0x83
REG_AMBI_PARM   = 0x84
REG_AMBI_DATA_H = 0x85
REG_AMBI_DATA_L = 0x86
REG_PROX_DATA_H = 0x87
REG_PROX_DATA_L = 0x88
REG_INT_CTRL    = 0x89
REG_INT_LOW_H   = 0x8A
REG_INT_LOW_L   = 0x8B
REG_INT_HIGH_H  = 0x8C
REG_INT_HIGH_H  = 0x8D
REG_INT_STAT    = 0x8E
REG_PROX_ADJ    = 0x8F

# Commands
CMD_SELFTIMED_EN = 0x01
CMD_PROX_EN      = 0x02
CMD_ALS_EN       = 0x04
CMD_PROX_OD      = 0x08
CMD_ALS_OD       = 0x10
CMD_PROX_DRDY    = 0x20
CMD_ALS_DRDY     = 0x40

# Proximity Measurement Rate
PROX_RATE_1      = 0x00
PROX_RATE_3      = 0x01
PROX_RATE_7      = 0x02
PROX_RATE_16     = 0x03
PROX_RATE_31     = 0x04
PROX_RATE_62     = 0x05
PROX_RATE_125    = 0x06
PROX_RATE_250    = 0x07

# Ambient Light Parameter
AMBI_CONT_CONV_MODE = 0x80
AMBI_RATE_1         = 0x00
AMBI_RATE_2         = 0x10
AMBI_RATE_3         = 0x20
AMBI_RATE_4         = 0x30
AMBI_RATE_5         = 0x40
AMBI_RATE_6         = 0x50
AMBI_RATE_8         = 0x60
AMBI_RATE_10        = 0x70
AMBI_AUTO_OFFSET    = 0x08
AMBI_AVE_NUM_1      = 0x00
AMBI_AVE_NUM_2      = 0x01
AMBI_AVE_NUM_4      = 0x02
AMBI_AVE_NUM_8      = 0x03
AMBI_AVE_NUM_16     = 0x04
AMBI_AVE_NUM_32     = 0x05
AMBI_AVE_NUM_64     = 0x06
AMBI_AVE_NUM_128    = 0x07

## smbus
bus = smbus.SMBus(1)

## FaBo Proximity I2C Controll class
class VCNL4010:

    ## Constructor
    #  @param [in] address VCNL4010 I2C slave address default:0x13
    def __init__(self, address=SLAVE_ADDRESS):
        self.address = address
        self.configuration()

    ## Search Device
    #  @retval true device connected
    #  @retval false device error
    def searchDevice(self):
        who_am_i = bus.read_byte_data(self.address, DEVID_REG)

        if who_am_i == DEVICE_ID:
            return true
        else:
            return false

    ## Configure Device
    def configuration(self):
        self.setCommand(
            CMD_SELFTIMED_EN |
            CMD_PROX_EN |
            CMD_ALS_EN
        )

        self.setProxRate(PROX_RATE_250)
        self.setLedCurrent(20)
        self.setAmbiParm(
            AMBI_RATE_10 |
            AMBI_AUTO_OFFSET |
            AMBI_AVE_NUM_128
        )

    ## Set Command Register
    #  @param [in] config Configure Parameter
    def setCommand(self, config):
        bus.write_byte_data(self.address, REG_CMD, config)

    ## Proximity Rate Register Setting
    #  @param [in] config Configure Parameter
    def setProxRate(self, config):
        bus.write_byte_data(self.address, REG_PROX_RATE, config)

    ## IR LED Current Setting
    #  @param [in] config Configure Parameter
    def setLedCurrent(self, config):
        bus.write_byte_data(self.address, REG_LED_CRNT, config)

    ## Ambient Light Parameter Register Setting
    # @param [in] config Configure Parameter
    def setAmbiParm(self, config):
        bus.write_byte_data(self.address, REG_AMBI_PARM, config)

    ## Check Proximity Data Ready
    #  @retval true Data is Ready
    #  @retval false Data is Not Ready
    def checkProxReady(self):
        data = bus.read_byte_data(self.address, REG_CMD)

        if data & CMD_PROX_DRDY:
            return true
        return false

    ## Check Ambient Light Data Ready
    #  @retval true  Data is Ready
    #  @retval false Data is Not Ready
    def checkAmbiReady(self):
        data = bus.read_byte_data(self.address, REG_CMD)

        if data & CMD_ALS_DRDY:
            return true
        return false

    ## Read Proximity Data
    #  @return [out] value Proximity Data
    def readProx(self):
        data = bus.read_i2c_block_data(self.address, REG_PROX_DATA_H, 2)
        return data[0]<<8 | data[1]

    ## Read Ambient Light Data
    #  @return value Ambient Light Data
    def readAmbi(self):
        data = bus.read_i2c_block_data(self.address, REG_AMBI_DATA_H, 2)
        return data[0]<<8 | data[1]

if __name__ == "__main__":
    proximity = VCNL4010()

    while True:
        prox = proximity.readProx()
        ambi = proximity.readAmbi()

        print "Prox = ", prox,
        print "Ambi = ", ambi,
        print
        time.sleep(1)
