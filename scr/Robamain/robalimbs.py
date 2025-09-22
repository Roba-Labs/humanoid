#!/usr/bin/python3
"""
This module defines the available limbs for the Roba robot.
"""

import numpy as np

class RobaLimbs:
    """
    A class to represent the limbs of the Roba robot.
    It contains a list of all the available limbs.
    """
    def __init__(self):
        """Initializes the RobaLimbs object."""
        self.limb_names = np.array([
            "camera3d",
            "trackingcam",
            "eyeled",
            "speak",
            "listening",
            "neckjoints",
            "righthand",
            "lefthand",
            "rightleg",
            "leftleg",
            "wheels"
        ])