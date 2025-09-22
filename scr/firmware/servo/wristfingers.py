import smbus2 as smbus
import time

# I2C Command Constants
# It's not clear what these commands mean without more context.
# Giving them descriptive names is a good first step.
CMD_POWER_OFF = 1
CMD_RF_CLOSE_GROUP = 8
CMD_RF_OPEN_GROUP = 9
CMD_LF_CLOSE_GROUP = 16
CMD_LF_OPEN_GROUP = 17

# These seem to be individual finger commands
CMD_RF_FINGER_1_CLOSE = 2
CMD_RF_FINGER_2_CLOSE = 4
CMD_RF_FINGER_3_CLOSE = 6
CMD_RF_FINGER_1_OPEN = 3
CMD_RF_FINGER_2_OPEN = 5
CMD_RF_FINGER_3_OPEN = 7

CMD_LF_FINGER_1_CLOSE = 10
CMD_LF_FINGER_2_CLOSE = 12
CMD_LF_FINGER_3_CLOSE = 14
CMD_LF_FINGER_1_OPEN = 11
CMD_LF_FINGER_2_OPEN = 13
CMD_LF_FINGER_3_OPEN = 15


class FingerController:
    """
    Controls the robot's fingers via I2C communication.
    """
    I2C_SLAVE_ADDRESS = 8  # Default I2C slave address

    def __init__(self, i2c_bus=1):
        """
        Initializes the FingerController.
        Args:
            i2c_bus (int): The I2C bus number.
        """
        self.i2c_bus = smbus.SMBus(i2c_bus)

    def power_off_motors(self):
        """Turns off the power to the finger motors."""
        self.send_command(CMD_POWER_OFF)

    def send_command(self, command, register=2):
        """
        Sends a command to the I2C slave.
        Args:
            command (int): The command to send.
            register (int): The register to write to.
        """
        self.i2c_bus.write_byte_data(self.I2C_SLAVE_ADDRESS, register, command)

    def close_left_fingers(self):
        """Closes the left hand fingers."""
        for cmd in [CMD_LF_FINGER_1_CLOSE, CMD_LF_FINGER_2_CLOSE, CMD_LF_FINGER_3_CLOSE]:
            self.send_command(cmd)
            time.sleep(0.02)
        time.sleep(1.5)
        self.send_command(CMD_LF_CLOSE_GROUP)

    def open_left_fingers(self):
        """Opens the left hand fingers."""
        self.send_command(CMD_LF_OPEN_GROUP)
        time.sleep(0.5)
        for cmd in [CMD_LF_FINGER_1_OPEN, CMD_LF_FINGER_2_OPEN, CMD_LF_FINGER_3_OPEN]:
            self.send_command(cmd)
            time.sleep(0.02)
        time.sleep(1.7)
        self.send_command(CMD_POWER_OFF)

    def close_right_fingers(self):
        """Closes the right hand fingers."""
        for cmd in [CMD_RF_FINGER_1_CLOSE, CMD_RF_FINGER_2_CLOSE, CMD_RF_FINGER_3_CLOSE]:
            self.send_command(cmd)
            time.sleep(0.02)
        time.sleep(1.5)
        self.send_command(CMD_RF_CLOSE_GROUP)

    def open_right_fingers(self):
        """Opens the right hand fingers."""
        self.send_command(CMD_RF_OPEN_GROUP)
        time.sleep(0.5)
        for cmd in [CMD_RF_FINGER_1_OPEN, CMD_RF_FINGER_2_OPEN, CMD_RF_FINGER_3_OPEN]:
            self.send_command(cmd)
            time.sleep(0.02)
        time.sleep(1.7)
        self.send_command(CMD_POWER_OFF)

    def close_bus(self):
        """Closes the I2C bus connection."""
        self.i2c_bus.close()