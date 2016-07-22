# coding: utf-8
## @package FaBoRTC_PCF2129
#  This is a library for the FaBo RTC I2C Brick.
#
#  http://fabo.io/215.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import smbus
import time

## I2C Slave Address PCF2129
SLAVE_ADDRESS = 0x51

# Register Addresses
CONTROL_REG   = 0x00
CONTROL_12_24 = 0x04
SECONDS       = 0x03
MINUTES       = 0x04
HOURS         = 0x05
DAYS          = 0x06
WEEKDAYS      = 0x07
MONTHS        = 0x08
YEARS         = 0x09

## smbus
bus = smbus.SMBus(1)

## FaBo RTC I2C Controll class
class PCF2129:

    ## Constructor
    #  @param [in] address PCF2129 I2C slave address default:0x51
    def __init__(self, address=SLAVE_ADDRESS):
        self.address = address

    ## Configure Device
    def configure(self):
        self.set24mode()

    ## Get Seconds from RTC
    #  @return seconds
    def getSeconds(self):
        data = bus.read_byte_data(self.address, SECONDS)
        return self.bcdToDec(data)

    ## Set Seconds to RTC
    #  @param [in] seconds seconds
    def setSeconds(self, seconds):
        if (seconds > 59) or (seconds < 0):
            seconds = 0

        data = decToBcd(seconds) + 0x80
        bus.write_byte_data(self.address, SECONDS, data)

    ## Get Minutes from RTC
    #  @return minutes
    def getMinutes(self):
        data = bus.read_byte_data(self.address, MINUTES)
        return self.bcdToDec(data)

    ## Set Minutes to RTC
    #  @param [in] minutes minutes
    def setMinutes(self, minutes):
        if (minutes > 59) or (minutes < 0):
            minutes = 0

        data = decToBcd(minutes)
        bus.write_byte_data(self.address, MINUTES, data)

    ## Get Hours from RTC
    #  @return hours
    def getHours(self):
        data = bus.read_byte_data(self.address, HOURS)
        return self.bcdToDec(data)

    ## Set Hours to RTC
    #  @param [in] hours hours
    def setHours(self, hours):
        self.set24mode()
        if (hours > 23) or (hours < 0):
            hours = 0

        data = decToBcd(hours)
        bus.write_byte_data(self.address, HOURS, data)

    ## Get Days from RTC
    #  @return days
    def getDays(self):
        data = bus.read_byte_data(self.address, DAYS)
        return self.bcdToDec(data)

    ## Set Days to RTC
    #  @param [in] days days
    def setDays(self, days):
        if (days > 31) or (days < 1):
            days = 1

        data = decToBcd(days)
        bus.write_byte_data(self.address, DAYS, data)

    ## Get Weekdays from RTC
    #  @return weekdays
    def getWeekdays(self):
        data = bus.read_byte_data(self.address, WEEKDAYS)
        return self.bcdToDec(data)

    ## Set Weekdays to RTC
    #  @param [in] weekdays weekdays
    def setWeekdays(self, weekdays):
        if (weekdays > 6) or (weekdays < 0):
            weekdays = 0

        data = decToBcd(weekdays)
        bus.write_byte_data(self.address, WEEKDAYS, data)


    ## Get Months from RTC
    #  @return months
    def getMonths(self):
        data = bus.read_byte_data(self.address, MONTHS)
        return self.bcdToDec(data)

    ## Set Months to RTC
    #  @param [in] months months
    def setMonths(self, months):
        if (months > 12) or (months < 1):
            months = 1
        data = decToBcd(months)
        bus.write_byte_data(self.address, MONTHS, data)

    ## Get Years from RTC
    #  @return years
    def getYears(self):
        data = bus.read_byte_data(self.address, YEARS)
        return self.bcdToDec(data)

    ## Set Years to RTC
    #  @param [in] years years
    def setYears(self, years):
        if (years > 99) and (years < 0):
            years = 0
        data = decToBcd(years)
        bus.write_byte_data(self.address, YEARS, data)

    ## Read from RTC
    #  @retval year   Read Years
    #  @retval month  Read Months
    #  @retval day    Read Days
    #  @retval hour   Read Hours
    #  @retval minute Read Minutes
    #  @retval second Read Seconds
    def now(self):
        data = bus.read_i2c_block_data(self.address, SECONDS, 7)

        seconds = self.bcdToDec(data[0])
        minutes = self.bcdToDec(data[1])
        hours   = self.bcdToDec(data[2])
        days    = self.bcdToDec(data[3])
        #  blank read weekdays
        months  = self.bcdToDec(data[5])
        years   = self.bcdToDec(data[6]) +2000

        return {'year':years, 'month':months, 'day':days, 'hour':hours, 'minute':minutes, 'second':seconds}

    ## Set to RTC
    #  @param [in] DateTime DateTime
    def setDate(self, years, months, days, hours, minutes, seconds):
        data = [
            self.decToBcd(seconds) | 0x80,
            self.decToBcd(minutes),
            self.decToBcd(hours),
            self.decToBcd(days),
            0x00,
            self.decToBcd(months),
            self.decToBcd(years-2000)
        ]
        bus.write_i2c_block_data(self.address, SECONDS, data)

    ## Set to 12 hour mode
    def set12mode(self):
        ctrl = self.readCtrl() | CONTROL_12_24
        self.writeCtrl(ctrl)

    ## Set to 24 hour mode
    def set24mode(self):
        ctrl = self.readCtrl() & ~(CONTROL_12_24)
        self.writeCtrl(ctrl)

    ## BCD to DEC
    #  @param [in] value BCD value
    #  @param [out] value DEC value
    def bcdToDec(self, value):
        return ((value / 16 * 10) + (value % 16))

    ## DEC to BCD
    #  @param [in] value DEC value
    #  @param [out] value BCD value
    def decToBcd(self, value):
        return ((value / 10 * 16) + (value % 10))

    ## Read Control Register
    #  @param [out] data register data
    def readCtrl(self):
        return bus.read_byte_data(self.address, CONTROL_REG)

    ## Write Control Register
    #  @param [in] data register data
    def writeCtrl(self, data):
        bus.write_byte_data(self.address, CONTROL_REG, data)
