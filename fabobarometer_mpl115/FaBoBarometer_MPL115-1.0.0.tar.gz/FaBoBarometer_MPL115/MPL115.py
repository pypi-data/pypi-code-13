# coding: utf-8
## @package FaBoBarometer_MPL115
#  This is a library for the FaBo Barometer I2C Brick.
#
#  http://fabo.io/204.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import smbus
import time

## MPL115A2 I2C slave address
SLAVE_ADDRESS = 0x60

# MPL115A2 Register Address
PADC_MSB = 0x00
PADC_LSB = 0x01
TADC_MSB = 0x02
TACD_LSB = 0x03
A0_MSB   = 0x04
A0_LSB   = 0x05
B1_MSB   = 0x06
B1_LSB   = 0x07
B2_MSB   = 0x08
B2_LSB   = 0x09
C12_MSB  = 0x0A
C12_LSB  = 0x0B
CONVERT  = 0x12

## SMBus
bus = smbus.SMBus(1)

## FaBo Barometer I2C Controll class
class MPL115:

    ## Constructor
    #  @param [in] address MPL115 I2C slave address default:0x60
    def __init__(self, address=SLAVE_ADDRESS):
        self.address = address
        self.readCoef()

    ## Read Coefficient Data
    def readCoef(self):
        data = bus.read_i2c_block_data(self.address, A0_MSB, 8)

        self.a0 = self.dataConv(data[1], data[0])
        self.b1 = self.dataConv(data[3], data[2])
        self.b2 = self.dataConv(data[5], data[4])
        self.c12 = self.dataConv(data[7], data[6])

        self.a0 =  float(self.a0) / (1<<3)
        self.b1 =  float(self.b1) / (1<<13)
        self.b2 =  float(self.b2) / (1<<14)
        self.c12 =  float(self.c12) / (1<<24)

    ## Read hpa
    #  @param [in] altitude Altitude defalut 0.0
    def readHpa(self, altitude = 0.0):
        data = self.readData()
        return data['hpa'] / pow(1.0 - (altitude /44330.0), 5.255)

    ## Read temperature
    #  @retval temp Read Temperature value
    def readTemp(self):
        data = self.readData()
        return data['temp']

    ## Read Measurement data
    #  @retval hpa hpa
    #  @retval temp temp
    def readData(self):

        bus.write_byte_data(self.address, CONVERT, 0x01)
        time.sleep(0.003)

        data = bus.read_i2c_block_data(self.address, PADC_MSB ,4)

        padc = ((data[0] << 8) | data[1]) >> 6
        tadc = ((data[2] << 8) | data[3]) >> 6

        pcomp = self.a0 + ( self.b1 + self.c12 * tadc ) * padc + self.b2 * tadc
        hpa  = pcomp * ( (1150.0-500.0)/1023.0 ) + 500.0
        temp = 25.0 - (tadc - 512.0 ) / 5.35

        return {'hpa':hpa, 'temp':temp}

    ## Data Convert
    # @param [in] self The object pointer.
    # @param [in] data1 LSB
    # @param [in] data2 MSB
    # @retval Value MSB+LSB(int 16bit)
    def dataConv(self, data1, data2):
        value = data1 | (data2 << 8)
        if(value & (1 << 16 - 1)):
            value -= (1<<16)
        return value

if __name__ == "__main__":
    barometer = MPL115()

    while True:
        data  = barometer.readData()
        a_hpa = barometer.readHpa(212.0)

        print "hpa  = ", data['hpa']
        print "temp = ", data['temp']
        print "hpa_aizu = ", a_hpa
        print
        time.sleep(1)
