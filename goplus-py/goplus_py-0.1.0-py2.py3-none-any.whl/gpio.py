#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


class GPIO():
    def __init__(self, platform, pin_number, pin_type):
        if platform == "rpi" or platform == "raspberrypi":
            print("RPi")
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BOARD)
            self.pin = GpioPyPin(pin_number, pin_type)
        elif platform == "edison":
            print("Intel Edison")
            import mraa
            self.pin = MraaPin(pin_number, pin_type)
        else:
            print("Unknown platform '%s', please use 'rpi' (Raspberry Pi) or 'edison' (Intel Edison)")
            sys.exit(1)

    def on(self):
        self.pin.on()

    def off(self):
        self.pin.off()


class MraaPin():
    def __init__(self, pin_number, pin_type):
        self.pin = mraa.Gpio(pin_number)
        self.pin_out = False
        if pin_type == 'output':
            self.pin_out = False
        elif pin_type == 'input':
            pass
        else:
            print("Unknown pin type '%s', please use 'input' or 'output'")
            sys.exit(1)
        if self.pin_out:
            self.pin.dir(mraa.DIR_OUT)
        else:
            self.pin.dir(mraa.DIR_IN)

    def on():
        self.pin.write(1)

    def off():
        self.pin.write(0)

    def read():
        if not self.pin_out:
            return self.pin.read()
        else:
            return None


class GpioPyPin():
    def __init__(self, pin_number, pin_type):
        self.pin = pin_number
        self.pin_out = False
        if pin_type == 'output':
            self.pin_out = False
        elif pin_type == 'input':
            pass
        else:
            print("Unknown pin type '%s', please use 'input' or 'output'")
            sys.exit(1)
        if self.pin_out:
            GPIO.setup(self.pin, GPIO.OUT)
        else:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def on():
        GPIO.output(self.pin, GPIO.HIGH)

    def off():
        GPIO.output(self.pin, GPIO.LOW)

    def read():
        if not self.pin_out:
            return GPIO.input(self.pin)
        else:
            return None
