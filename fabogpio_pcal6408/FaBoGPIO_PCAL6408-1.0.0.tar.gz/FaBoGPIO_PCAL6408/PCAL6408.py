# coding: utf-8
## @package FaBoGPIO_PCAL6408.py
#  This is a library for the FaBo GPIO I2C Brick.
#
#  http://fabo.io/210.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import smbus
import time

# Default I2C Slave Address
SLAVE_ADDRESS = 0x20

## Register Addresses
OUTPUT_REG        = 0x01
CONFIGURATION_REG = 0x03

## OUTPUT Parameter
IO0_OUTPUT = 0b00000000
IO0_INPUT  = 0b00000001
IO1_OUTPUT = 0b00000000
IO1_INPUT  = 0b00000010
IO2_OUTPUT = 0b00000000
IO2_INPUT  = 0b00000100
IO3_OUTPUT = 0b00000000
IO3_INPUT  = 0b00001000
IO4_OUTPUT = 0b00000000
IO4_INPUT  = 0b00010000
IO5_OUTPUT = 0b00000000
IO5_INPUT  = 0b00100000
IO6_OUTPUT = 0b00000000
IO6_INPUT  = 0b01000000
IO7_OUTPUT = 0b00000000
IO7_INPUT  = 0b10000000

IO0        = 0b00000001
IO1        = 0b00000010
IO2        = 0b00000100
IO3        = 0b00001000
IO4        = 0b00010000
IO5        = 0b00100000
IO6        = 0b01000000
IO7        = 0b10000000

## smbus
bus = smbus.SMBus(1)

## FaBo GPIO I2C Controll class
class PCAL6408:

    ## Constructor
    #  @param [in] address PCAL6408 I2C slave address default:0x20
    def __init__(self, address=SLAVE_ADDRESS):

        self.address = address
        self.output  = 0x00
        self.configuration()

    ## Configure Device
    def configuration(self):
        conf = IO0_OUTPUT | IO1_OUTPUT | IO2_OUTPUT | IO3_OUTPUT | IO4_OUTPUT | IO5_OUTPUT | IO6_OUTPUT | IO7_OUTPUT
        bus.write_byte_data(self.address, CONFIGURATION_REG, conf)

    ## set Port to Digital
    #  @param [in] port Port
    #  @param [in] output output 1:HIGH, 0:LOW
    def setDigital(self, port, output):
        if output == 1:
            self.output |= port
        elif (output == 0):
            self.output &= ~port
        bus.write_byte_data(self.address, OUTPUT_REG, self.output)

    ## All Port to LOW
    def setAllClear(self):
        bus.write_byte_data(self.address, OUTPUT_REG, 0x00)
        self.output = 0x00

    ## set Port to GPIO
    #  @param [in] output output
    def setGPIO(self, output):
        bus.write_byte_data(self.address, OUTPUT_REG, output)
