# coding: utf-8
## @package FaBo3Axis_ADXL345
#  This is a library for the FaBo 3AXIS I2C Brick.
#
#  http://fabo.io/201.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import smbus
import time

## ADXL345 SLAVE_ADDRESS
SLAVE_ADDRESS   = 0x53
## Who_am_i register
DEVID_REG       = 0x00
## Device id
DEVICE          = 0xe5
## data format register
DATA_FORMAT     = 0x31
## powr control register
POWER_CTL       = 0x2d
## get 3axis register
DATA_XYZ        = 0x32
## Tap Threshold
THRESH_TAP_REG  = 0x1D
## Tap Duration
DUR_REG         = 0x21
## Tap Latency
LATENT_REG      = 0x22
## Tap Window
WINDOW_REG      = 0x23
## interrupt MAP
INT_MAP_REG     = 0x2F
## interrupt Enable
INT_ENABLE_REG  = 0x2E
## Power-saving features control
POWER_CTL_REG   = 0x2D
## Source of Single Tap/Double Tap
TAP_STATUS_REG  = 0x2B
## Axis Control for Single Tap/Double Tap
TAP_AXES_REG    = 0x2A
## Source of Interrupts
INT_SOURCE_REG  = 0x30
## Data Format Control
DATA_FORMAT_REG = 0x31

# Data Format Param
## SELF Test ON
SELF_TEST_ON   = 0b10000000
## SELF Test OFF
SELF_TEST_OFF  = 0b00000000
## SELF SPI ON
SPI_ON         = 0b01000000
## SELF SPI OFF
SPI_OFF        = 0b00000000
## INT_INVERT ON
INT_INVERT_ON  = 0b00100000
## INT_INVERT OFF
INT_INVERT_OFF = 0b00000000
## FULL_RES ON
FULL_RES_ON    = 0b00001000
## FULL_RES OFF
FULL_RES_OFF   = 0b00000000
## JUSTIFY ON
JUSTIFY_ON     = 0b00000100
## JUSTIFY OFF
JUSTIFY_OFF    = 0b00000000
## RANGE 16G
RANGE_16G      = 0b00000011
## RANGE 8G
RANGE_8G       = 0b00000010
## RANGE 4G
RANGE_4G       = 0b00000001
## RANGE 2G
RANGE_2G       = 0b00000000

# Data Format Param
## Axis Tap Control Z axis ON
TAP_AXES_Z_ON  = 0b00000001
## Axis Tap Control Y axis ON
TAP_AXES_Y_ON  = 0b00000010
## Axis Tap Control X axis ON
TAP_AXES_X_ON  = 0b00000100
## Axis Interrupt Single Tap
INT_SINGLE_TAP = 0b01000000
## Axis Interrupt Double Tap
INT_DOUBLE_TAP = 0b00100000

# Power Control Param
## AUTO SLEEP ON
AUTO_SLEEP_ON  = 0b00010000
## AUTO SLEEP OFF
AUTO_SLEEP_OFF = 0b00000000
## AUTO MEASURE ON
MEASURE_ON     = 0b00001000
## AUTO MEASURE OFF
MEASURE_OFF    = 0b00000000
## SLEEP ON
SLEEP_ON       = 0b00000100
## SLEEP OFF
SLEEP_OFF      = 0b00000000
## WAKEUP 1Hz
WAKEUP_1HZ     = 0b00000011
## WAKEUP 2Hz
WAKEUP_2HZ     = 0b00000010
## WAKEUP 4Hz
WAKEUP_4HZ     = 0b00000001
## WAKEUP 8Hz
WAKEUP_8HZ     = 0b00000000

## SMBus
bus = smbus.SMBus(1)

## ADXL345 I2C Controll class
class ADXL345:

    ## Constructor
    #  @param [in] address ADXL345 i2c slave_address default:0x53
    def __init__(self, address=SLAVE_ADDRESS):
        self.address = address

        self.configuration()
        self.powerOn()

    ## Device check
    #  @param [in] self The object pointer.
    #  @retval true  : found
    #  @retval false : Not found
    def searchDevice(self):
        who_am_i = bus.read_byte_data(self.address, DEVID_REG)

        if(who_am_i == DEVICE):
            return True
        else:
            return False

    ## Set configuration
    #  @param [in] self The object pointer.
    def configuration(self):
        conf = SELF_TEST_OFF | SPI_OFF | INT_INVERT_OFF | FULL_RES_OFF | JUSTIFY_OFF | RANGE_16G
        bus.write_byte_data(self.address, DATA_FORMAT_REG, conf)

    ## ADXL345 Power On
    #  @param [in] self The object pointer.
    def powerOn(self):
        power = AUTO_SLEEP_OFF | MEASURE_ON | SLEEP_OFF | WAKEUP_8HZ
        bus.write_byte_data(self.address, POWER_CTL_REG, power)

    ## Enable Tap
    #  @param [in] self The object pointer.
    #  @param [in] thresh_tap  TAPの強さの閾値       Default:0x32
    #  @param [in] dur         TAP持続時間          Default:0x30
    #  @param [in] latant      識別間隔             Default:0xf8
    #  @param [in] window      識別間隔のインターバル Default:0x10
    def enableTap(self, thresh_tap=0x32, dur=0x30, latant=0xf8, window=0x10):
        bus.write_byte_data(self.address, THRESH_TAP_REG, thresh_tap) # 62.5mg/LBS
        bus.write_byte_data(self.address, DUR_REG, dur)               # 1.25ms/LSB
        bus.write_byte_data(self.address, LATENT_REG, latant)         # 1.25ms/LSB
        bus.write_byte_data(self.address, WINDOW_REG, window)         # 1.25ms/LSB

        int_tap = INT_SINGLE_TAP | INT_DOUBLE_TAP
        bus.write_byte_data(self.address, INT_ENABLE_REG, int_tap)     # Interrupts Tap Enable
        bus.write_byte_data(self.address, TAP_AXES_REG, TAP_AXES_Z_ON) # Tap Enable z axis

    ## Read Tap Status
    # @param [in] self The object pointer.
    # @return byte interrupts Status
    def readIntStatus(self):
        return bus.read_byte_data(self.address, INT_SOURCE_REG)

    ## check SingleTap
    # @param [in] self The object pointer.
    # @param [in] value : interrupts Status
    # @retval true  : Tap
    # @retval false : Not Tap
    def isSingleTap(self, value):
        if((value & INT_SINGLE_TAP) == INT_SINGLE_TAP):
            return True
        else:
            return False

    ## check DoubleTap
    # @param [in] self The object pointer.
    # @param [in] value : interrupts Status
    # @retval true  : Tap
    # @retval false : Not Tap
    def isDoubleTap(self, value):
        if((value & INT_DOUBLE_TAP) == INT_DOUBLE_TAP):
            return True
        else:
            return False

    ## Read 3axis data
    # @param [in] self The object pointer.
    # @retval x : x-axis data
    # @retval y : y-axis data
    # @retval z : z-axis data
    def read(self):
        data = bus.read_i2c_block_data(self.address, DATA_XYZ, 6)

        x = self.dataConv(data[0], data[1])
        y = self.dataConv(data[2], data[3])
        z = self.dataConv(data[4], data[5])

        return {"x":x, "y":y, "z":z}

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
    axis = ADXL345()

    while True:
        axis_value = axis.read()
        print "x = ", (axis_value['x'])
        print "y = ", (axis_value['y'])
        print "z = ", (axis_value['z'])
        print
        time.sleep(1)
