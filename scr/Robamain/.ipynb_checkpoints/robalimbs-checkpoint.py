#!/usr/bin/python3

import numpy as np
class Limbs:
    def __init__(self):
        self.lims=np.array([
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
      
        #self.lims.shape= (0,np.size(self.lims))