# coding: utf-8
## @package FaBoLCD_PCF8574
#  This is a library for the FaBo LCD I2C Brick.
#
#  http://fabo.io/212.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import smbus
import time

## PCF8574 Default I2C Slave Address
SLAVE_ADDRESS      = 0x20

# commands
LCD_CLEARDISPLAY   = 0x01
LCD_RETURNHOME     = 0x02
LCD_ENTRYMODESET   = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT    = 0x10
LCD_FUNCTIONSET    = 0x20
LCD_SETCGRAMADDR   = 0x40
LCD_SETDDRAMADDR   = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT          = 0x00
LCD_ENTRYLEFT           = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON   = 0x04
LCD_DISPLAYOFF  = 0x00
LCD_CURSORON    = 0x02
LCD_CURSOROFF   = 0x00
LCD_BLINKON     = 0x01
LCD_BLINKOFF    = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE  = 0x00
LCD_MOVERIGHT   = 0x04
LCD_MOVELEFT    = 0x00

# flags for function set
LCD_8BITMODE    = 0x10
LCD_4BITMODE    = 0x00

LCD_2LINE       = 0x08
LCD_1LINE       = 0x00

LCD_5x10DOTS    = 0x04
LCD_5x8DOTS     = 0x00

# pin/port bit
RS  = 0b00000001 # P0 : RS bit
RW  = 0b00000010 # P1 : R/W bit
EN  = 0b00000100 # P2 : Enable bit
BL  = 0b00001000 # P3 : BACKLIGHT bit
DB4 = 0b00010000 # P4 : DB4 bit
DB5 = 0b00100000 # P5 : DB5 bit
DB6 = 0b01000000 # P6 : DB6 bit
DB7 = 0b10000000 # P7 : DB7 bit

## smbus
bus = smbus.SMBus(1)

## FaBoLCDmini_AQM0802A LCD I2C Controll class
class PCF8574:

# When the display powers up, it is configured as follows:
#
# 1. Display clear
# 2. Function set:
#    DL = 1; 8-bit interface data
#    N = 0; 1-line display
#    F = 0; 5x8 dot character font
# 3. Display on/off control:
#    D = 0; Display off
#    C = 0; Cursor off
#    B = 0; Blinking off
# 4. Entry mode set:
#    I/D = 1; Increment by 1
#    S = 0; No shift
#
# Note, however, that resetting the Arduino doesn't reset the LCD, so we
# can't assume that its in that state when a sketch starts (and the
# LiquidCrystal constructor is called).

    ## Constructor
    #  @param [in] address PCF8574 I2C slave address default:0x20
    def __init__(self, address=SLAVE_ADDRESS):
        self.address   = address
        self.backlight = BL
        self.displayfunction = LCD_4BITMODE | LCD_1LINE | LCD_5x8DOTS
        self.begin()

    ## begin
    #  @param [in] cols    LCD col     Default:16
    #  @param [in] lines   LCD lines   Default:2
    #  @param [in] dotsize LCD Dotsize Default:0x10(8dots)
    def begin(self, cols=16, lines=2, dotsize=LCD_5x8DOTS):
        if lines > 1:
            self.displayfunction |= LCD_2LINE
        self.numlines = lines

        self.setRowOffsets(0x00, 0x40, 0x00 + cols, 0x40 + cols)

        # for some 1 line displays you can select a 10 pixel high font
        if (dotsize != LCD_5x8DOTS) and (lines == 1):
            self.displayfunction |= LCD_5x10DOTS

        # SEE PAGE 45/46 FOR INITIALIZATION SPECIFICATION!
        # according to datasheet, we need at least 40ms after power rises above 2.7V
        # before sending commands. Arduino can turn on way before 4.5V so we'll wait 50
        time.sleep(0.05)
        # Now we pull both RS and R/W low to begin commands
        self.writeI2c(0x00)

        # thi/ is according to the hitachi HD44780 datasheet
        # figure 24, pg 46

        # we start in 8bit mode, try to set 4 bit mode
        self.write4bits(DB4|DB5)
        time.sleep(0.0045) # wait min 4.1ms

        # second try
        self.write4bits(DB4|DB5)
        time.sleep(0.0045) # wait min 4.1ms

        # third go!
        self.write4bits(DB4|DB5)
        time.sleep(0.00015)

        # finally, set to 4-bit interface
        self.write4bits(DB5)

        # finally, set # lines, font size, etc.
        self.command(LCD_FUNCTIONSET | self.displayfunction)

        # turn the display on with no cursor or blinking default
        self.displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.display()

        # clear it off
        self.clear()

        # Initialize to default text direction (for romance languages)
        self.displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
        # set the entry mode
        self.command(LCD_ENTRYMODESET | self.displaymode)

    ## setRowOffsets
    #  @param [in] row0
    #  @param [in] row1
    #  @param [in] row2
    #  @param [in] row3
    def setRowOffsets(self, row0, row1, row2, row3):
        self.row_offsets = [row0, row1, row2, row3]

# high level commands, for the user!

    ## Display clear
    def clear(self):
        self.command(LCD_CLEARDISPLAY)  # clear display, set cursor position to zero
        time.sleep(0.002)    #this command takes a long time!

    ## move home point
    def home(self):
        self.command(LCD_RETURNHOME)  # set cursor position to zero
        time.sleep(0.002)    #this command takes a long time!

    ## setCursor
    def setCursor(self, col, row):
        max_lines = len(self.row_offsets)
        if row >= max_lines:
            row = max_lines - 1        # we count rows starting w/0

        if row >= self.numlines:
            row = self.numlines - 1    # we count rows starting w/0

        self.command(LCD_SETDDRAMADDR | (col + self.row_offsets[row]))

    ## Turn the display off (quickly)
    def noDisplay(self):
        self.displaycontrol &= ~LCD_DISPLAYON
        self.command(LCD_DISPLAYCONTROL | self.displaycontrol)

    ## Turn the display on (quickly)
    def display(self):
        self.displaycontrol |= LCD_DISPLAYON
        self.command(LCD_DISPLAYCONTROL | self.displaycontrol)

    ## Turns the underline cursor off
    def noCursor(self):
        self.displaycontrol &= ~LCD_CURSORON
        self.command(LCD_DISPLAYCONTROL | self.displaycontrol)

    ## Turns the underline cursor on
    def cursor(self):
        self.displaycontrol |= LCD_CURSORON
        self.command(LCD_DISPLAYCONTROL | self.displaycontrol)

    ## Turn off the blinking cursor
    def noBlink(self):
        self.displaycontrol &= ~LCD_BLINKON
        self.command(LCD_DISPLAYCONTROL | self.displaycontrol)

    ## Turn on the blinking cursor
    def blink(self):
        self.displaycontrol |= LCD_BLINKON
        self.command(LCD_DISPLAYCONTROL | self.displaycontrol)

    # These commands scroll the display without changing the RAM
    def scrollDisplayLeft(self):
        self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)

    ## These commands scroll the display without changing the RAM
    def scrollDisplayRight(self):
        self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)

    ## This is for text that flows Left to Right
    def leftToRight(self):
        self.displaymode |= LCD_ENTRYLEFT
        self.command(LCD_ENTRYMODESET | self.displaymode)

    ## This is for text that flows Right to Left
    def rightToLeft(self):
        self.displaymode &= ~LCD_ENTRYLEFT
        self.command(LCD_ENTRYMODESET | self.displaymode)

    ## This will 'right justify' text from the cursor
    def autoscroll(self):
        self.displaymode |= LCD_ENTRYSHIFTINCREMENT
        self.command(LCD_ENTRYMODESET | self.displaymode)

    ## This will 'left justify' text from the cursor
    def noAutoscroll(self):
        self.displaymode &= ~LCD_ENTRYSHIFTINCREMENT
        self.command(LCD_ENTRYMODESET | self.displaymode)

    ## Allows us to fill the first 8 CGRAM locations with custom characters
    def createChar(self, location, charmap):
        location &= 0x7 # we only have 8 locations 0-7
        self.command(LCD_SETCGRAMADDR | (location << 3))
        for char in charmap:
            self.writeCreateChar(char)

# mid level commands, for sending data/cmds

    ## command
    def command(self, value):
        self.send(value, 0)

    ## write
    #  @param [in] data string ,number, list Output data
    def write(self, data):
        if isinstance(data, (int, long, float)):
            out_str = str(data)
        else:
            out_str = data

        for chr in out_str:

            if isinstance(chr, (int, long, float)):
                out_chr = str(chr)
            else:
                out_chr = chr

            for c in out_chr:
                self.send(ord(c), RS)

        return 1  # assume sucess

    ## writeInt
    #  @param [in]  Output int
    def writeCreateChar(self, int):

        self.send(int, RS)

        return 1  # assume sucess

# low level data pushing commands

    ## write either command or data, 4-bit
    #  @param [in] value write value
    #  @param [in] mode  write mode
    def send(self, value, mode):
        Hbit = value & 0xF0
        Lbit = (value << 4) & 0xF0
        self.write4bits(Hbit|mode)
        self.write4bits(Lbit|mode)

    ## pulseEnable
    #  @param [in] value write value
    def pulseEnable(self, value):
        self.writeI2c(value & ~EN)  # EN LOW
        time.sleep(0.000000045)     # enable pulse must be >450ns
        self.writeI2c(value|EN)     # EN HIGH
        time.sleep(0.000000045)     # enable pulse must be >450ns
        self.writeI2c(value & ~EN)  # EN LOW
        time.sleep(0.0000100)       # commands need > 37us to settle

    ## write4bits
    #  @param [in] value write value
    def write4bits(self, value):
        self.writeI2c(value)
        self.pulseEnable(value)

    ## writeI2c
    #  @param [in] data write data
    def writeI2c(self, data):
        bus.write_byte(self.address, data | self.backlight)
