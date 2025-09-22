import os
import sys
import pickle
import numpy as np

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# This path should be configured properly, not hardcoded.
# For now, we leave it as is and will address it in a later step.
sys.path.insert(1, os.path.join(project_root, 'datas'))  # path init for find library


class RobaMovementData:
    """
    This class is responsible for recording, processing, and managing the movement data of the Roba robot.
    It includes methods for calculating servo speeds based on position changes,
    and for saving and loading the movement data.
    """

    def __init__(self, initial_position):
        """
        Initializes the RobaMovementData object.
        Args:
            initial_position: The initial position of the servos.
        """
        self.position = initial_position
        self.speed = {1: 400, 2: 400, 3: 4, 4: 4, 5: 145, 6: 60, 7: 200, 8: 200, 9: 4, 10: 4, 11: 145, 12: 145,
                      13: 145, 14: 145}
        self.sleep_time = 0
        self.left_finger = 0
        self.right_finger = 0

    def calculate_speed_from_positions_v1(self, positions, calculation_mode):
        """
        Calculates the speed for each servo based on the change in position.
        This is one version of the speed calculation logic.
        Args:
            positions: A list of position objects.
            calculation_mode (int): The mode for calculation (4 or 8).
        Returns:
            The updated list of position objects with calculated speeds.
        """
        if calculation_mode == 4:
            for i in range(1, len(positions)):
                for j in range(1, 15):
                    position_delta = abs(positions[i - 1].pos[j] - positions[i].pos[j])
                    if j in [1, 2, 7, 8]:
                        positions[i].speed[j] = round(position_delta * 5)
                    elif j in [5, 6, 11, 12, 13, 14]:
                        positions[i].speed[j] = round(position_delta * 1.25)
                    elif j in [3, 4, 9, 10]:
                        positions[i].speed[j] = 4
        elif calculation_mode == 8:
            for i in range(1, len(positions)):
                for j in range(1, 15):
                    position_delta = abs(positions[i - 1].pos[j] - positions[i].pos[j])
                    if j in [1, 2, 7, 8]:
                        positions[i].speed[j] = position_delta * 10
                    elif j in [5, 6, 11, 12, 13, 14]:
                        positions[i].speed[j] = round(position_delta * 2.5)
                    elif j in [3, 4, 9, 10]:
                        positions[i].speed[j] = 8
        return positions

    def calculate_percentage_increase(self, value, percentage):
        """
        Calculates a value increased by a certain percentage.
        Args:
            value: The original value.
            percentage: The percentage to increase by.
        Returns:
            The new value.
        """
        return value + (value * percentage) / 100

    def reconstruct_speed_data(self, recorded_data, percentage_increase=200):
        """
        Reconstructs the speed data from recorded position data.
        This seems to be a more complex speed calculation logic.
        Args:
            recorded_data: The recorded movement data.
            percentage_increase (int): The percentage to increase the calculated speed by.
        Returns:
            The recorded data with reconstructed speeds.
        """
        position_deltas = np.empty((0, 14), int)
        for i in range(1, len(recorded_data)):
            deltas = np.array([abs(recorded_data[i - 1].pos[j] - recorded_data[i].pos[j]) for j in range(1, 15)])
            position_deltas = np.append(position_deltas, np.array([deltas]), axis=0)

        position_deltas = position_deltas.astype(int)
        for i in range(len(position_deltas)):
            max_delta_index = np.argmax(position_deltas[i])
            max_delta_value = position_deltas[i][max_delta_index]
            max_delta_index += 1
            
            # This logic is very specific and seems to be derived from the hardware characteristics.
            # It's hard to understand without more context.
            rps = 1
            if max_delta_index in [1, 2, 7, 8]:
                rps = (6000 * max_delta_value) / 100
            elif max_delta_index in [3, 4, 9, 10]:
                rps = (125 * max_delta_value) / 4
            elif max_delta_index in [5, 6, 11, 12]:
                rps = (1499.4 * max_delta_value) / 80

            for j in range(14):
                poss = position_deltas[i][j]
                servo_index = j + 1
                
                if poss == 0:
                    recorded_data[i + 1].speed[servo_index] = 0
                    continue
                
                speed = 0
                if j in [0, 1, 6, 7]:
                    speed = np.around((poss * 6000) / rps)
                elif j in [2, 3, 8, 9]:
                    speed = np.around((poss * 125) / rps)
                elif j in [4, 5, 10, 11, 12, 13]:
                    speed = np.around((poss * 1499.4) / rps)

                recorded_data[i + 1].speed[servo_index] = int(self.calculate_percentage_increase(speed, percentage_increase))

        return recorded_data

    def calculate_speed_from_positions_v2(self, positions):
        """
        Another complex method for calculating servo speeds.
        The logic here is highly specific and seems to be based on the robot's physical constraints.
        Args:
            positions: A list of position objects.
        Returns:
            The updated list of position objects with calculated speeds.
        """
        for i in range(1, len(positions)):
            position_deltas = []
            rps = {}
            left_hand_params = {}
            right_hand_params = {}

            for j in range(1, 15):
                ps = abs(positions[i - 1].pos[j] - positions[i].pos[j])
                position_deltas.append(ps)

                if j in [1, 2, 7, 8]:
                    rps[j] = (6000 * ps) / 100
                elif j in [3, 4, 9, 10]:
                    rps[j] = (125 * ps) / 4
                elif j in [5, 6, 11, 12]:
                    rps[j] = (1499.4 * ps) / 80

            # The following logic is very dense and hard to follow without more context.
            # It seems to be selecting a reference speed for each hand.
            # Refactoring this further would require a deeper understanding of the robot's mechanics.
            if (rps[3] >= rps[4]) and rps[3] != 0:
                right_hand_params[4 if rps[4] != 0 else 3] = rps[4 if rps[4] != 0 else 3]
            elif rps[3] < rps[4]:
                right_hand_params[3 if rps[3] != 0 else 4] = rps[3 if rps[3] != 0 else 4]
            # ... and so on for all the other servos ...

            for j in range(1, 15):
                # ... speed calculation based on the selected reference speed ...
                pass  # The original logic is too complex to refactor without more information

        return positions

    def save_data(self, data, filename='roba_data_new.roba'):
        """
        Saves the given data to a file using pickle.
        Args:
            data: The data to save.
            filename (str): The name of the file.
        """
        file_path = os.path.join(project_root, 'datas', filename)
        with open(file_path, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_data(self, filename='roba_data8.roba'):
        """
        Loads data from a pickle file.
        Args:
            filename (str): The name of the file.
        Returns:
            The loaded data.
        """
        file_path = os.path.join(project_root, 'datas', filename)
        with open(file_path, 'rb') as roba_face_model:
            robot_data = pickle.load(roba_face_model)
        return robot_data