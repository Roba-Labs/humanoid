#!/usr/bin/python3
"""
This script is the main control program for the Roba robot.
It defines classes for managing robot applications and their associated limbs (hardware components).
"""

import sys
import os
import threading

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add the required directories to the python path
sys.path.insert(1, os.path.join(project_root, 'scr', 'Robamain'))
sys.path.insert(1, os.path.join(project_root, 'scr', 'Roba_conversion_ai'))
sys.path.insert(1, os.path.join(project_root, 'scr', 'Roba_vision'))
sys.path.insert(1, os.path.join(project_root, 'scr', 'firmware', 'servo'))
import time
import pickle
import numpy as np
import smbus2 as smbus
import Jetson.GPIO as GPIO
from IPython.display import clear_output

import ASR
import robaaibot
import Speak2rpi
from robalimbs import RobaLimbs
from motor_init import ServoController
from roba_record import RobaMovementData
from wristfingers import FingerController
import tracking
from camera3D import RealSenseCamera


class RobaApp:
    """
    Represents a single application running on the Roba robot.
    An application can utilize various limbs of the robot, such as hands, head, vision, and chat.
    """

    def __init__(self, name):
        """
        Initializes the RobaApp.
        Args:
            name (str): The name of the application.
        """
        self.name = name
        self.initialized_limbs = np.array([])
        self.is_conversational_ai_enabled = True
        self.asr_service = None
        self.speaker = None
        self.robachatbot = None
        self.servo_motor = None
        self.motor_ids = None
        self.hand_head_data = None
        self.finger = None
        self.track = None
        self.roba_camera = None

    def initialize_chat(self, tts_server_ip="192.168.0.120"):
        """
        Initializes the chat functionality, including the chatbot, speech recognition, and speaker.
        Args:
            tts_server_ip (str): The IP address of the Text-to-Speech server.
        """
        self.robachatbot = robaaibot.RobaChatbot()
        time.sleep(0.2)
        self.speaker = Speak2rpi.TextToSpeechClient(tts_server_ip)
        time.sleep(0.5)
        self.speaker.received_data = "Paused"

    def run_conversational_ai(self):
        """
        The main loop for the conversational AI.
        Listens for voice input, gets a response from the chatbot, and speaks the response.
        """
        play_time = 0
        self.asr_service = ASR.SpeechToText()
        self.answer_text = ""
        while self.is_conversational_ai_enabled:
            text_query = ""
            time.sleep(0.2)

            if self.speaker.received_data == "Paused":
                play_time = 0
                text_query = self.asr_service.get_recognized_text()

                if not text_query or text_query.isspace():
                    text_query = "&"
                    self.asr_service.clear_recognized_text()
                    self.asr_service.is_listening = True

                if text_query != "&" and len(text_query) > 1 and text_query != "['']":
                    self.asr_service.clear_recognized_text()
                    print(text_query)
                    self.answer_text = self.robachatbot.get_answer(text_query)
                    text_query = "&"
                    self.answer_text = str(self.answer_text)
                    if len(self.answer_text) > 1 and self.answer_text != "['']":
                        self.speaker.speak_text(self.answer_text)
                        start_time = time.time()

                        while self.speaker.received_data != "Playing":
                            time.sleep(0.1)
                            if time.time() - start_time > 5:
                                break
                        start_time = time.time()
                        while self.speaker.received_data != "Paused":
                            self.asr_service.is_listening = False
                            time.sleep(0.1)
                            if time.time() - start_time > 50:
                                break
                        self.asr_service.is_listening = True
                        time.sleep(1.5)
                        self.asr_service.clear_recognized_text()
                else:
                    self.asr_service.is_listening = True
                    self.asr_service.clear_recognized_text()

        print("Exiting Conversational AI")

    def start_chat_thread(self):
        """Starts the conversational AI in a separate thread."""
        self.is_conversational_ai_enabled = True
        cai_thread = threading.Thread(target=self.run_conversational_ai, daemon=True)
        cai_thread.start()

    def initialize_limb(self, limb_name):
        """
        Initializes a specific limb of the robot.
        Args:
            limb_name (str): The name of the limb to initialize.
        """
        if limb_name == "handhead":
            self.servo_motor = ServoController()
            self.motor_ids = self.servo_motor.get_all_servo_ids()
        elif limb_name == "handheadstore":
            self.hand_head_data = RobaMovementData(self.servo_motor.init_postion)
        elif limb_name == "fingers":
            self.finger = FingerController()
        elif limb_name == "tracker":
            self.track = tracking.Track()
            for _ in range(5):
                clear_output(True)
                print(self.track.RPY)
                print(self.track.trans)
                time.sleep(0.1)
        elif limb_name == "vision":
            self.roba_camera = RealSenseCamera()
            time.sleep(1)
        elif limb_name == "chat":
            self.initialize_chat()
            self.start_chat_thread()

    def initialize_all_limbs(self):
        """Initializes all the limbs that have been added to the application."""
        for name in self.initialized_limbs:
            self.initialize_limb(name)

    def add_limb(self, limb_name):
        """
        Adds a limb to the application and initializes it.
        Args:
            limb_name (str): The name of the limb to add.
        """
        self.initialized_limbs = np.append(self.initialized_limbs, limb_name)
        self.initialize_limb(limb_name)

    def get_right_hand_pose(self):
        """Returns the position and speed of the motors in the right hand."""
        motor_positions = self.servo_motor.get_hand_position(self.motor_ids[0:7])
        motor_speeds = {i: self.servo_motor.smotor[i] for i in range(1, 8)}
        return [motor_positions, motor_speeds]

    def get_left_hand_pose(self):
        """Returns the position and speed of the motors in the left hand."""
        motor_positions = self.servo_motor.get_hand_position(self.motor_ids[7:13])
        motor_speeds = {i: self.servo_motor.smotor[i] for i in range(7, 13)}
        return [motor_positions, motor_speeds]

    def get_head_pose(self):
        """Returns the position and speed of the motors in the head."""
        motor_positions = self.servo_motor.get_hand_position(self.motor_ids[13:15])
        motor_speeds = {i: self.servo_motor.mspeed[i] for i in range(13, 15)}
        return [motor_positions, motor_speeds]

    def get_servo_positions(self, key):
        """
        Returns the positions of the specified servos.
        Args:
            key: The IDs of the servos.
        """
        motor_positions = self.servo_motor.get_hand_position(key)
        return motor_positions

    def get_all_servo_positions_and_speeds(self):
        """Returns the positions and speeds of all servos."""
        motor_positions = self.servo_motor.get_hand_position(self.motor_ids)
        return [motor_positions, self.servo_motor.mspeed]

    def initialize_servo_motors_to_default(self):
        """Sets all servo motors to their initial positions."""
        self.servo_motor.set_hand_position(self.servo_motor.mID, self.servo_motor.init_postion, self.servo_motor.mspeed)

    def get_runtime_limb_data(self, name, key):
        """
        Provides a way to control the different limbs of the robot at runtime.
        Args:
            name (str): The name of the limb.
            key: The command or data for the limb.
        Returns:
            The data from the limb, or 0 if the command is not recognized.
        """
        if name == "righthand":
            if key == "readpos":
                return self.get_right_hand_pose()
        elif name == "lefthand":
            if key == "readpos":
                return self.get_left_hand_pose()
        elif name == "head":
            if key == "readpos":
                return self.get_head_pose()
        elif name == "allservo":
            if key == "readpos":
                return self.get_all_servo_positions_and_speeds()
        elif name == "servoespos":
            return self.get_servo_positions(key)
        elif name == "handreleaseall":
            self.servo_motor.release_motors(self.motor_ids)
        elif name == "handrelease":
            self.servo_motor.release_motors(key)
        elif name == "handinit":
            self.initialize_servo_motors_to_default()
        elif name == "rightfinger":
            if key == "open":
                self.finger.open_right_fingers()
            elif key == "close":
                self.finger.close_right_fingers()
        elif name == "leftfinger":
            if key == "open":
                self.finger.open_left_fingers()
            elif key == "close":
                self.finger.close_left_fingers()
        elif name == "fingeroff":
            self.finger.power_off_motors()
        elif name == "send_finger_command":
            for k in key:
                self.finger.send_command(k)
                time.sleep(0.02)
        elif name == "tracker":
            if key == "rpy":
                return self.track.RPY
            elif key == "trans":
                return self.track.trans
        elif name == "vision":
            if key == "0":
                img, ver = self.roba_camera.get_frames()
                return [img, ver]
            else:
                img, ver = self.roba_camera.get_frames()
                return [img, ver]
        return 0

    def add_limb_data(self, limb_name, data):
        """
        Adds data for a specific limb.
        Note: This method seems incomplete and only handles 'handhead'.
        """
        if limb_name == "handhead":
            if self.hand_head_data is not None:
                self.hand_head_data.append(data)


class Roba:
    """Manages the robot's applications."""

    def __init__(self):
        """Initializes the Roba Manager."""
        self.available_limbs = RobaLimbs().limb_names.tolist()
        self.roba_apps = {}

    def create_app(self, name):
        """
        Creates a new RobaApp.
        Args:
            name (str): The name for the new application.
        """
        self.roba_apps[name] = RobaApp(name)

    def list_apps(self):
        """Returns a list of the names of all created applications."""
        return list(self.roba_apps.keys())

    def get_app_runtime_data(self, app_name, limb, key):
        """
        Gets runtime data from a limb of a specific application.
        Args:
            app_name (str): The name of the application.
            limb (str): The name of the limb.
            key: The command or data for the limb.
        Returns:
            The data from the limb.
        """
        roba_app = self.roba_apps[app_name]
        app_data = roba_app.get_runtime_limb_data(limb, key)
        return app_data

    def add_limbs_to_app(self, app_name, limb_name):
        """
        Adds a limb to a specific application.
        Args:
            app_name (str): The name of the application.
            limb_name (str): The name of the limb to add.
        """
        roba_app = self.roba_apps[app_name]
        roba_app.add_limb(limb_name)

    def initialize_app_limbs(self, app_name):
        """
        Initializes all limbs for a given application.
        Args:
            app_name (str): The name of the application.
        """
        roba_app = self.roba_apps[app_name]
        roba_app.initialize_all_limbs()

    def print_app_info(self, name):
        """
        Prints information about an application, including its initialized limbs.
        Args:
            name (str): The name of the application.
        """
        roba_app = self.roba_apps[name]
        print("..........app limbs.........")
        print(" ")
        print(roba_app.initialized_limbs.tolist())
        print(" ")

    def deactivate_app_limbs(self, app_name, limb_name):
        """
        Deactivates a specific limb of an application.
        Args:
            app_name (str): The name of the application.
            limb_name (str): The name of the limb to deactivate.
        """
        roba_app = self.roba_apps[app_name]
        if limb_name == "handhead":
            if roba_app.servo_motor:
                roba_app.servo_motor.close()
        elif limb_name == "handheadstore":
            roba_app.hand_head_data = None
        elif limb_name == "fingers":
            if roba_app.finger:
                roba_app.finger.close_bus()
        elif limb_name == "tracker":
            if roba_app.track:
                roba_app.track.break_loop = False
        elif limb_name == "vision":
            if roba_app.roba_camera:
                roba_app.roba_camera.stop_pipeline()
        elif limb_name == "chat":
            roba_app.is_conversational_ai_enabled = False


# Example of how to use the classes
# def main():
#     rb_manager = RobaManager()
#     print(rb_manager.available_limbs)
#     rb_manager.create_app("test_app")
#     rb_manager.add_limbs_to_app("test_app", "chat")
#
# if __name__ == "__main__":
#     main()

# The following lines seem to be for saving an application instance to a file.
# appname = name + ".rap"
# with open(appname, 'wb') as roba_app_file:
#     pickle.dump(robaapp, roba_app_file)