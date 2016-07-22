# coding: utf-8
## @package FaBoColor_S11059
#  This is a library for the FaBo Color I2C Brick.
#
#  http://fabo.io/203.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import smbus
import time

SLAVE_ADDRESS = 0x2A

CONTROL      = 0x00
TIMING_H     = 0x01
TIMING_L     = 0x02
DATA_RED_H   = 0x03
DATA_RED_L   = 0x04
DATA_GREEN_H = 0x05
DATA_GREEN_L = 0x06
DATA_BLUE_H  = 0x07
DATA_BLUE_L  = 0x08
DATA_IR_H    = 0x09
DATA_IR_L    = 0x0A

# S11059 Control bits
CTRL_RESET   = 0x80
CTRL_SLEEP   = 0x40
CTRL_GAIN    = 0x08
CTRL_MODE    = 0x04

# S11059 Measurement time select
CTRL_TIME_875U  = 0x0
CTRL_TIME_14M   = 0x1
CTRL_TIME_224M  = 0x2
CTRL_TIME_1792M = 0x3

# S11059 Gain select
GAIN_HIGH   = 1
GAIN_LOW    = 0

# S11059 Mode select
MODE_MANUAL = 1
MODE_FIXED  = 0

## SMBus
bus = smbus.SMBus(1)

## FaBo Color I2C Controll class
class S11059:

    ## Constructor
    #  @param [in] address S11059 I2C slave address default:0x2a
    def __init__(self, address=SLAVE_ADDRESS):

        self.address = address
        self.restart() # wake from sleep
        self.setGain(GAIN_HIGH)
        self.setMode(MODE_FIXED)
        self.setTime(CTRL_TIME_224M)

    ## Set Gain
    #  @param [in] gain Gain
    def setGain(self, gain):
        data = self.getConfig()
        if gain == GAIN_HIGH:
            data |= CTRL_GAIN
        else:
            data &= ~(CTRL_GAIN)
        bus.write_byte_data(self.address, CONTROL, data)

    ## Set Mode
    #  @param [in] mode Mode
    def setMode(self, mode):
        self.mode = mode
        data = self.getConfig()

        if mode == MODE_MANUAL:
            data |= CTRL_MODE
        else:
            data &= ~(CTRL_MODE)
        bus.write_byte_data(self.address, CONTROL, data)

    ## Set Time
    #  @param [in] itime Time
    def setTime(self, itime):
        self.itime = itime

        data = self.getConfig()
        data &= 0xFC
        data |= itime
        bus.write_byte_data(self.address, CONTROL, data)

    ## Start Measurement
    def start(self):
        data = self.getConfig()
        data &= 0x3F # RESET off,SLEEP off
        bus.write_byte_data(self.address, CONTROL, data)

    ## Restart Measurement
    def restart(self):

        data = self.getConfig()
        data = 0x80 # RESET on,SLEEP off
        data &= 0xBF
        bus.write_byte_data(self.address, CONTROL, data)

        time.sleep(0.001)
        data = self.getConfig()
        data = 0x3F # RESET off,SLEEP off
        bus.write_byte_data(self.address, CONTROL, data)

    ## Set Manual Timing
    #  @param [in] timing timing
    def setManualTiming(self, timing):
        data = [
            (timing >> 8) & 0xFF,
            timing & 0xFF
        ]

        bus.write_byte_data(self.address, TIMING_H, data)

    ## Get Manual Timing
    #  @param [out] timing timing
    def getManualTiming(self):
        data = bus.read_i2c_block_data(self.address, TIMING_H, 2)
        return (data[0] << 8) | data[1]

    ## Get Config
    #  @param [out] config contorl bits
    def getConfig(self):
        data = bus.read_byte_data(self.address, CONTROL)
        return data

    ## Sleep check
    #  @retval true device sleep
    #  @retval false device running
    def checkSleep(self):
        data = bus.read_i2c_block_data(self.address, CONTROL, 1)
        return data & 0x20

    ## Wait device sleep
    def waitAdc(self):
        print "waitAdc start"
        while self.checkSleep()== False:
            time.sleep(1/1000000) # 1 microsecond
        time.sleep(0.001)
        print "waitAdc end"

    ## Read Measurement data
    #  @retval r red value
    #  @retval g green value
    #  @retval b blue value
    #  @retval i IR value
    def read(self):
        if self.mode == MODE_MANUAL:
            print "self.restart() start"
            self.restart() # wake from sleep
            print "waitADC start"
            self.waitAdc() # wait measure
            print "waitACD end"
        else:
            if self.itime == CTRL_TIME_875U:         # delay 88usec
                time.sleep(88*4/1000000)  # micro second
                time.sleep(0.001)         # wait buffer

            elif self.itime == CTRL_TIME_14M:   # delay 1.4msec
                time.sleep(2 * 4/1000)
                time.sleep(0.001)         # wait buffer

            elif self.itime == CTRL_TIME_224M:       # delay 22.4msec
                time.sleep(23 * 4/1000)
                time.sleep(0.001)         # wait buffer
            elif self.itime == CTRL_TIME_1792M: # delay 179.2msec
                time.sleep(180 * 4/1000)
                time.sleep(0.001)         # wait buffer
        data = bus.read_i2c_block_data(self.address, DATA_RED_H, 8)
        r = (data[0] << 8) | data[1]
        g = (data[2] << 8) | data[3]
        b = (data[4] << 8) | data[5]
        ir = (data[6] << 8) | data[7]
        return {'r':r, 'g':g, 'b':b, 'ir':ir}

if __name__ == "__main__":
    color = S11059()

    while True:
        rgb = color.read()
        print "r =", (rgb['r']),
        print " g =", (rgb['g']),
        print " B =", (rgb['b']),
        print " ir =", (rgb['ir'])
        print
        time.sleep(1)
