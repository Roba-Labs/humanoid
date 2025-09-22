import os
import sys
import time
import copy
import numpy as np
import serial.tools.list_ports
from scservo_sdk import PortHandler, PacketHandler, COMM_SUCCESS, SCS_LOWORD, SCS_HIWORD

# --- Constants ---
# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# This path should be configured properly, not hardcoded.
sys.path.insert(1, os.path.join(project_root, 'scr', 'firmware', 'servo'))

# Control Table Addresses
ADDR_TORQUE_ENABLE = 40
ADDR_GOAL_ACC = 41
ADDR_GOAL_POSITION = 42
ADDR_GOAL_SPEED = 46
ADDR_PRESENT_POSITION = 56
ADDR_PRESENT_TIME = 44

# Default Settings
DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 1000000
MOVING_ACCELERATION = 0
SCS_PROTOCOL_END = 0  # 0 for STS/SMS, 1 for SCS

# Motor Configurations
MOTOR_TYPES = {1: "sms", 2: "sms", 3: "sms", 4: "sms", 5: "scs", 6: "scs", 7: "sms", 8: "sms", 9: "sms",
               10: "sms", 11: "scs", 12: "scs", 13: "scs", 14: "scs"}
MOTOR_SPEEDS = {1: 400, 2: 400, 3: 12, 4: 15, 5: 145, 6: 60, 7: 400, 8: 400, 9: 12, 10: 12, 11: 145,
                12: 145, 13: 145, 14: 145}
JOINT_LIMITS = [[0, 0, 0],
                [275, 60, 340], [326, 175, 326], [180, 35, 355], [345, 250, 345], [150, 80, 225],
                [130, 55, 215], [135, 70, 350], [99, 99, 250], [215, 40, 360], [90, 90, 185],
                [150, 80, 225], [200, 115, 275], [225, 134, 315], [175, 111, 225]]


class ServoController:
    """
    Controls the servo motors of the Roba robot using the scservo_sdk.
    Handles initialization, setting positions, speeds, and reading sensor data.
    """

    def __init__(self, port=DEFAULT_SERIAL_PORT, baudrate=DEFAULT_BAUDRATE):
        """
        Initializes the ServoController.
        Args:
            port (str): The serial port for communication.
            baudrate (int): The baudrate for the serial communication.
        """
        self.port_handler = PortHandler(port)
        self.packet_handler = PacketHandler(SCS_PROTOCOL_END)

        if not self.port_handler.openPort():
            raise IOError("Failed to open the port")
        if not self.port_handler.setBaudRate(baudrate):
            raise IOError("Failed to change the baudrate")

        self.motor_ids = self.get_all_servo_ids()
        self.initial_positions = {mid: JOINT_LIMITS[mid][0] for mid in self.motor_ids}
        print("Initial positions:", self.initial_positions)
        self.initialize_motors()

    def initialize_motors(self):
        """Sets the motors to their initial positions."""
        self.set_hand_position(self.motor_ids, self.initial_positions, MOTOR_SPEEDS)

    def set_hand_speed(self, motor_ids, motor_speeds):
        """
        Sets the speed for the specified motors.
        Args:
            motor_ids (list): A list of motor IDs.
            motor_speeds (dict): A dictionary mapping motor IDs to speeds.
        """
        for motor_id in motor_ids:
            speed = motor_speeds.get(motor_id, 0)
            self.packet_handler.write2ByteTxRx(self.port_handler, motor_id, ADDR_GOAL_SPEED, speed)

    # --- Angle Conversion Utilities ---
    @staticmethod
    def sms_to_degrees(value):
        return round((360 * value) / 4095)

    @staticmethod
    def degrees_to_sms(degrees):
        return round((4095 * degrees) / 360)

    @staticmethod
    def scs_to_degrees(value):
        return round((360 * value) / 1023)

    @staticmethod
    def degrees_to_scs(degrees):
        return round((1023 * degrees) / 360)

    def set_hand_position(self, motor_ids, positions, speeds):
        """
        Sets the position for the specified motors.
        Args:
            motor_ids (list): A list of motor IDs.
            positions (dict): A dictionary mapping motor IDs to positions (in degrees).
            speeds (dict): A dictionary mapping motor IDs to speeds.
        """
        for motor_id in motor_ids:
            position = positions.get(motor_id, 0)
            speed = speeds.get(motor_id, 0)
            
            # Enforce joint limits
            min_pos, max_pos = JOINT_LIMITS[motor_id][1], JOINT_LIMITS[motor_id][2]
            position = max(min_pos, min(position, max_pos))

            packet_handler = PacketHandler(0 if MOTOR_TYPES[motor_id] == "sms" else 1)
            pos_in_servo_units = self.degrees_to_sms(position) if MOTOR_TYPES[motor_id] == "sms" else self.degrees_to_scs(position)

            packet_handler.write1ByteTxRx(self.port_handler, motor_id, ADDR_GOAL_ACC, MOVING_ACCELERATION)
            packet_handler.write2ByteTxRx(self.port_handler, motor_id, ADDR_GOAL_SPEED, speed)
            packet_handler.write2ByteTxRx(self.port_handler, motor_id, ADDR_GOAL_POSITION, pos_in_servo_units)
        
        # Wait for movement to complete
        # This is a simple way to wait. A more advanced implementation would check if the motors are still moving.
        time.sleep(1)

    def get_hand_position(self, motor_ids):
        """
        Gets the current position of the specified motors.
        Args:
            motor_ids (list): A list of motor IDs.
        Returns:
            dict: A dictionary mapping motor IDs to their current positions in degrees.
        """
        positions = {}
        for motor_id in motor_ids:
            packet_handler = PacketHandler(0 if MOTOR_TYPES[motor_id] == "sms" else 1)
            pos_speed, _, _ = packet_handler.read2ByteTxRx(self.port_handler, motor_id, ADDR_PRESENT_POSITION)
            position_in_servo_units = SCS_LOWORD(pos_speed)

            if MOTOR_TYPES[motor_id] == "sms":
                positions[motor_id] = self.sms_to_degrees(position_in_servo_units)
            else:
                positions[motor_id] = self.scs_to_degrees(position_in_servo_units)
        return positions

    def get_all_servo_ids(self):
        """
        Pings the bus to find all connected servo IDs.
        Returns:
            list: A list of all detected servo IDs.
        """
        all_ids = []
        for i in range(15):  # Assuming max 15 servos
            if self.packet_handler.ping(self.port_handler, i)[1] == COMM_SUCCESS:
                all_ids.append(i)
        return all_ids

    def release_motors(self, motor_ids):
        """
        Disables the torque for the specified motors.
        Args:
            motor_ids (list): A list of motor IDs to release.
        """
        for motor_id in motor_ids:
            packet_handler = PacketHandler(0 if MOTOR_TYPES[motor_id] == "sms" else 1)
            packet_handler.write1ByteTxRx(self.port_handler, motor_id, ADDR_TORQUE_ENABLE, 0)

    def close(self):
        """Closes the serial port connection."""
        self.port_handler.closePort()
