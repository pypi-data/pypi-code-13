from .i2c_bus import bus
from .tcs3472 import tcs3472
from .bmp280 import bmp280
from .ads1015 import ads1015
from .lsm303d import lsm303d
from .leds import leds

leds = leds()
light = tcs3472(bus)
weather = bmp280(bus)
analog = ads1015(bus)
motion = lsm303d(bus)
