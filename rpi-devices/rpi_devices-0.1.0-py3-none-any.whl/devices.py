import RPi.GPIO as GPIO
from time import sleep

"""This module provides classes for various devices to be used along with a Raspberry Pi.
Each device comes with a few common methods to control the device.
"""

__all__ = ['cleanup', 'DCMotor', 'SimpleMotor', 'Servo', 'LED']

def cleanup():
    """Same as RPi.GPIO.cleanup()"""
    GPIO.cleanup()

class DCMotor(object):
    """DC Motor which is connected to a controller (L293D or similar)

    Use this class for a DC motor whose rotation speed needs to be controlled.
    Typically, the Pi's GPIO will be connected to the pins of a L293D or similar controller,
    and the controller is connected to the motor.
    """

    __A = -1
    __B = -1
    __E = -1
    __pwm = None
    __mode = GPIO.BOARD

    def __init__(self, a, b, en, mode=GPIO.BOARD):
        """Construct a new 'DCMotor' object.

        Args:
            a: GPIO pin number connected to A pin of the motor controller
            b: GPIO pin number connected to B pin of the motor controller
            en: GPIO pin number connected to the EN pin of the motor controller
            mode: GPIO pin numbering mode, RPi.GPIO.BCM or RPi.GPIO.BOARD (default)

        Raises:
            ValueError: If mode is not RPi.GPIO.BCM or RPi.GPIO.BOARD
        """

        if mode == GPIO.BOARD or mode == GPIO.BCM:
            self.__mode = mode
        else:
            raise ValueError("'mode' should be RPi.GPIO.BOARD or RPi.GPIO.BCM")
        self.__A = a
        self.__B = b
        self.__E = en
        GPIO.setmode(mode)
        GPIO.setup(a, GPIO.OUT)
        GPIO.setup(b, GPIO.OUT)
        GPIO.setup(en, GPIO.OUT)
        self.__pwm = GPIO.PWM(en, 100)
        self.__pwm.start(0)

    def swap():
        """Swap the forward and backward directions

        No need to change any circuit connections
        """

        temp = self.__A
        self.__A = self.__B
        self.__B = temp

    def forward(self, dc):
        """Rotates the motor in an arbitrary direction.

        The directions depend on the circuit connections and so cannot be guaranteed.
        Only guarantee is that forward and backward methods will always rotate in opposite directions.
        """

        GPIO.setmode(__mode)
        GPIO.output(self.__A, GPIO.HIGH)
        GPIO.output(self.__B, GPIO.LOW)
        if (0 <= dc <= 100):
            self.__pwm.ChangeDutyCycle(dc)

    def backward(self, dc):
        """Rotates the motor in an arbitrary direction.

        The directions depend on the circuit connections and so cannot be guaranteed.
        Only guarantee is that forward and backward methods will always rotate in opposite directions.
        """

        GPIO.setmode(__mode)
        GPIO.output(self.__A, GPIO.LOW)
        GPIO.output(self.__B, GPIO.HIGH)
        if (0 <= dc <= 100):
            self.__pwm.ChangeDutyCycle(dc)

    def stop(self):
        """Stops the motor

        This has no effect if motor is not rotating.
        """

        GPIO.setmode(__mode)
        self.__pwm.stop()

    def change_speed(self, dc):
        """Changes the speed of rotation of motor.

        Manipulates the duty cycle of the internal software PWM to change the rotation speed.
        Higher the duty cycle, faster the speed of rotation.

        Args:
            dc: Duty cycle to change to

        Raises:
            ValueError: 0 <= dc <= 100 is not True
        """

        if (0 <= dc <= 100):
            GPIO.setmode(__mode)
            self.__pwm.ChangeDutyCycle(dc)
        else:
            raise ValueError("dc must be between 0 and 100")

    def get_settings(self):
        """Returns a dictionary of GPIO pins being used and the mode of setup

        Dictionary contains the following keys:
            MODE: Mode being used by the object as string
            A: GPIO pin connected to pin A of the motor controller
            B: GPIO pin connected to pin B of the motor controller
            EN: GPIO pin connected to enabler pin of the motor controller
        """

        return {'MODE': 'BOARD' if __mode == GPIO.BOARD else 'BCM', 'A': __A, 'B': __B, 'EN': __EN}

class Servo(object):
    """Servo motor 

    Use this object for a servo connected to the Raspberry Pi
    """

    __P = -1
    __pwm = None
    __zero = 3
    __slope = 0.04722
    __restrictions = [0, 360]
    __mode = GPIO.BOARD

    def __init__(self, p, mode=GPIO.BOARD, freq=50, zero=3, slope=0.04722, lower=0, upper=360):
        """Construct a new Servo object

        For most standard servos, the default inputs will work, except when 0 postion needs to
        be changed or a specific PWM frequency is required

        Args:
            p: GPIO pin connected to the control pin of the servo
            mode: GPIO pin numbering mode, RPi.GPIO.BCM or RPi.GPIO.BOARD (default)
            freq: Frequency of internal PWM (default: 50)
            zero: Zero degree position duty cycle (default: 3)
            slope: Slope of the function that translates duty cycles to position (default: 0.04722)
            lower: Lower limit on the position of servo in degrees (default: 0)
            upper: Upper limit on the position of servo in degrees (default: 360)

        Raises:
            ValueError: If mode is not RPi.GPIO.BCM or RPi.GPIO.BOARD or lower and upper values don't make sense
        """

        if mode == GPIO.BCM or mode == GPIO.BOARD:
            self.__mode = mode
        else:
            raise ValueError("'mode' should be RPi.GPIO.BOARD or RPi.GPIO.BCM")

        self.__P = p
        self.change_restrictions(lower, upper)
        self.__zero = zero
        self.__slope = slope
        GPIO.setmode(mode)
        GPIO.setup(p, GPIO.OUT)
        self.__pwm = GPIO.PWM(p, freq)
        self.__pwm.start(7.25)

    def config(self, d0, d180):
        """Configure the servo positions
        
        Resets the 0 position of servo and the recalculates the slope
        Note that there is no way to confirm the actual positions of the servo,
        so passing bad inputs to this can lead to undefined behavior of turn method

        Args:
            d0: New 0 degree position duty cycle
            d180: New 180 degree position duty cycle

        Raises:
            ValueError: If d180 < d0 or either value is negative or zero
        """

        if (d180 > d0 > 0):
            self.__slope = (d180 - d0) / 180
            self.__zero = d0
        else:
            raise ValueError("d180 > d0 > 0 should be True")

    def change_freq(self, freq):
        """Changes the frequency of the internal PWM

        After this, the servo will probably need to be reconfigured using config method

        Args:
            freq: The new frequency for the internal PWM
        
        Raises:
            ValueError: If frequency is negative or zero
        """

        if (freq > 0):
            GPIO.setmode(__mode)
            self.__pwm.ChangeFrequency(freq)

    def change_duty_cycle(self, dc):
        """Changes the duty cycle of the internal PWM

        Also sets the servo to the position for that duty cycle
        Can be used for obtaining d0 and d180 for the config method

        Args:
            dc: New duty cycle of the internal PWM

        Raises:
            ValueError: If duty cycle is not between 0 and 100, both inclusive
        """

        if (0 <= dc <= 100):
            GPIO.setmode(__mode)
            self.__pwm.ChangeDutyCycle(dc)
        else:
            raise ValueError("0 <= dc <= 100 must be True")

    def change_restrictions(self, lower, upper):
        """Changes the limits between which the servo can be set

        Args:
            lower: Lower limit on the position of servo in degrees
            upper: Upper limit on the position of servo in degrees 

        Raises:
            ValueError: If lower and upper values don't make sense
        """

        if (0 <= lower <= upper <= 360):
            self.__restrictions = [lower, upper]
        else:
            raise ValueError("lower and upper values should be between 0 and 360, and upper >= lower")

    def turn(self, angle):
        """Turn the servo to the specified angle

        If angle is not between the limits set during construction or using change_restrictions later,
        servo is set to closest limit position

        Args:
            angle: Angle of desired position of the servo
        """

        if (self.__restrictions[0] <= angle <= self.__restictions[1]):
            GPIO.setmode(__mode)
            self.__pwm.ChangeDutyCycle((float(angle) * self.__slope) + self.__zero)
        elif (0 <= angle < self.__restrictions[0]): 
            self.turn(self.__restrictions[0])
        elif (self.__restrictions[1] < angle <= 360): 
            self.turn(self.__restrictions[1])
        else:
            pass

    def get_settings(self):
        """Returns a dictionary of the settings of the servo

        Dictionary contains the following keys:
            MODE: Mode being used by the object as string
            P: GPIO pin connected to the control pin of the servo
            LOWER: Lower limit on the position of the servo in degrees
            UPPER: Upper limit on the position of the servo in degrees
        """

        return {
            'MODE': 'BOARD' if __mode == GPIO.BOARD else 'BCM',
            'P': __P,
            'LOWER': __restrictions[0],
            'UPPER': __restrictions[1]
       }

class SimpleMotor(object):
    """DC motor which does not require speed control

    Use this object for a DC motor which does not need to be controlled
    using PWM
    """

    __A = -1
    __B = -1
    __mode = GPIO.BOARD

    def __init__(self, a, b, mode=GPIO.BOARD):
        """Construct a new 'DCMotor' object.

        Args:
            a: GPIO pin number connected to one of the motor pins, directly or via a controller
            b: GPIO pin number connected to the other motor pin, directly or via a controller
            mode: GPIO pin numbering mode, RPi.GPIO.BCM or RPi.GPIO.BOARD (default)

        Raises:
            ValueError: If mode is not RPi.GPIO.BCM or RPi.GPIO.BOARD
        """

        if mode == GPIO.BOARD or mode == GPIO.BCM:
            self.__mode = mode
        else:
            raise ValueError("'mode' should be RPi.GPIO.BOARD or RPi.GPIO.BCM")
        self.__A = a
        self.__B = b
        GPIO.setmode(mode)
        GPIO.setup(a, GPIO.OUT)
        GPIO.setup(b, GPIO.OUT)

    def forward(self):
        """Rotates the motor in an arbitrary direction.

        The directions depend on the circuit connections and so cannot be guaranteed.
        Only guarantee is that forward and backward methods will always rotate in opposite directions.
        """

        GPIO.output(self.__A, GPIO.HIGH)
        GPIO.output(self.__B, GPIO.LOW)

    def backward(self):
        """Rotates the motor in an arbitrary direction.

        The directions depend on the circuit connections and so cannot be guaranteed.
        Only guarantee is that forward and backward methods will always rotate in opposite directions.
        """

        GPIO.output(self.__A, GPIO.LOW)
        GPIO.output(self.__B, GPIO.HIGH)

    def stop(self):
        """Stops the motor

        This has no effect if motor is not rotating.
        """

        GPIO.output(self.__A, GPIO.LOW)
        GPIO.output(self.__B, GPIO.LOW)

    def swap(self):
        """Swap the forward and backward directions

        No need to change any circuit connections
        """

        temp = self.__A
        self.A = self.__B
        self.B = temp

    def get_settings(self):
        """Returns a dictionary of GPIO pins being used and the mode of setup

        Dictionary contains the following keys:
            MODE: Mode being used by the object as string
            A: GPIO pin connected to pin A of the motor controller
            B: GPIO pin connected to pin B of the motor controller
        """

        return {'MODE': 'BOARD' if __mode == GPIO.BOARD else 'BCM', 'A': __A, 'B': __B}


class LED(object):
    """Light Emitting Diode attached to the Pi

    Use this class for LEDs, Laser Diodes or any other single pin controlled device for which
    the methods provided make sense
    """

    __PIN = -1
    __mode = GPIO.BOARD

    def __init__(self, pin, mode=GPIO.BOARD):
        """Constructs a LED object

        Args:
            pin: GPIO pin of the Pi connected to diode
            mode: GPIO pin numbering mode, RPi.GPIO.BCM or RPi.GPIO.BOARD (default)

        Raises:
            ValueError: If mode is not RPi.GPIO.BCM or RPi.GPIO.BOARD
        """

        if mode == GPIO.BOARD or mode == GPIO.BCM:
            self.__mode = mode
        else:
            raise ValueError("'mode' should be RPi.GPIO.BOARD or RPi.GPIO.BCM")
        self.__PIN = pin
        GPIO.setmode(mode)
        GPIO.setup(pin, GPIO.OUT)

    def on(self):
        """Turns on the LED"""

        GPIO.setmode(__mode)
        GPIO.output(self.__PIN, GPIO.HIGH)

    def off(self):
        """Turns off the LED"""

        GPIO.setmode(__mode)
        GPIO.output(self.__PIN, GPIO.LOW)

    def flash(self, duration = 0.01):
        """Flashes the LED once

        Args:
            duration: Duration of the flash in seconds (default: 0.01 seconds)
        """

        self.on()
        sleep(duration)
        self.off()

    def blink(self, blinks, duration = 0.1, interval = 0.1):
        """Blinks the LED for specified number of times

        Args:
            blinks: Number of time the LED will go on and off
            duration: Duration in seconds for the LED to stay on (default: 0.1 seconds)
            interval: Interval in seconds between LED turning off and turning back on (default: 0.1 seconds)
        """

        for i in range(1, blinks + 1):
            self.flash(duration = duration)
            sleep(interval)

    def get_settings():
        """Returns a dictionary of the pin and mode of the LED

        Dictionary contains the following keys:
            MODE: Mode being used by the object as string
            P: GPIO pin connected to the LED
        """

        return {'MODE': 'BOARD' if __mode == GPIO.BOARD else 'BCM', 'P': __PIN}
