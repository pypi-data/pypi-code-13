# Register addresses
MPU6050_ADDRESS = 0xD0
PWR_MGMT_1      = 0x6B
PWR_MGMT_2      = 0x6C
MOT_THR         = 0x1F
INT_PIN_CFG     = 0x37
INT_ENABLE      = 0x38
ACCEL_XOUT_H    = 0x3B
ACCEL_YOUT_H    = 0x3D
ACCEL_ZOUT_H    = 0x3F
TEMP_OUT_H      = 0x41
GYRO_XOUT_H     = 0x43
GYRO_YOUT_H     = 0x45
GYRO_ZOUT_H     = 0x47

# Masks
MOT_EN       = 0x40 # Enable motion interrupt
INT_LEVEL    = 0x80 # Active-low INT
INT_OPEN     = 0x40 # Open-drain INT
LP_WAKE_CTRL = 0xC0 # Frequency of wake-ups in Accelerometer Only Low Power Mode.
STBY_XA      = 0x20 # X-axis acceleromter standby
STBY_YA      = 0x10 # Y-axis acceleromter standby
STBY_ZA      = 0x08 # Z-axis acceleromter standby
STBY_XG      = 0x04 # X-axis gyro standby
STBY_YG      = 0x02 # Y-axis gyro standby
STBY_ZG      = 0x01 # Z-axis gyro standby

def init_imu(SCL, SDA):
    i2cInit(True, SCL, SDA)
    write_imu_data(PWR_MGMT_1, chr(0x00)) # Wake up the IMU
    write_imu_data(MOT_THR, chr(150))  # Set the motion detection threshold
    prev = read_imu_data(INT_ENABLE, 1)
    write_imu_data(INT_ENABLE, prev | MOT_EN) # Enable the motion interrupt
    prev = read_imu_data(INT_PIN_CFG, 1)
    write_imu_data(INT_PIN_CFG, prev | INT_LEVEL | INT_OPEN) # INT is active low, open drain
    prev = read_imu_data(PWR_MGMT_2, 1)
    write_imu_data(PWR_MGMT_2, prev | STBY_XG | STBY_YG| STBY_ZG) # Disable gyro

def get_imu_gryo(axis):
    """Get the gyroscope rotational velocity value for the given axis.

        Arguments:
            axis (string): Axis to retrieve value for - "x", "y", or "z"

        Returns:
            int: Rotational velocity for axis from -32768 to 32767 for
                 -250deg/s to 250deg/sec
    """
    if axis == "x":
        axis_command = GYRO_XOUT_H
    elif axis == "y":
        axis_command = GYRO_YOUT_H
    elif axis == "z":
        axis_command = GYRO_ZOUT_H
    else:
        return 0

    return _get_sensor_reading(axis_command)

def get_imu_accel(axis):
    """Get the acceleration value for the given axis.

        Arguments:
            axis (string): Axis to retrieve value for - "x", "y", or "z"

        Returns:
            int: Acceleration value for axis from -32768 to 32767 for -2g to 2g
    """
    if axis == "x":
        axis_command = ACCEL_XOUT_H
    elif axis == "y":
        axis_command = ACCEL_YOUT_H
    elif axis == "z":
        axis_command = ACCEL_ZOUT_H
    else:
        return 0

    return _get_sensor_reading(axis_command)

def _get_sensor_reading(command):
    """Get a 2-byte reading from the IMU and convert to an integer.

    Arguments:
        command (int): Command to collect reading for

    Returns:
        int: Integer value of the collected reading
    """

    val = read_imu_data(command, 2)

    # Need to convert the hi/lo byte string to an integer:
    return ord(val[0]) << 8 | ord(val[1])

def write_imu_data(registerAddress, data):
    slaveAddress = MPU6050_ADDRESS
    cmd = ""
    cmd += chr( slaveAddress )
    cmd += chr( registerAddress )
    cmd += data
    i2cWrite(cmd, 10, False)

def read_imu_data(registerAddress, bytes):
    slaveAddress = MPU6050_ADDRESS
    cmd = ""
    cmd += chr( slaveAddress )
    cmd += chr( registerAddress )
    i2cWrite(cmd, 10, False)

    cmd = ""
    cmd += chr( slaveAddress | 1 )
    retval = i2cRead(cmd, bytes, 10, False)

    return retval
