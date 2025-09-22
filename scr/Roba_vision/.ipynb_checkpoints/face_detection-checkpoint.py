import copy
import os
import pickle

import cv2
import face_recognition
import numpy as np
import torch


class Roba_Faces_recognition:

        def __init__(self):
             
           
           with open('RFVmodle3.rbf', 'rb') as roba_face_model:
              self.RFVmodl=pickle.load(roba_face_model)
          
        def name_to_color(self,name):
            color = [(ord(c.lower())-97)*8 for c in name[:3]]
            return color
        
        def find_faces(self,image):

            self.locations = face_recognition.face_locations(image, model=MODEL)
            self.encodings = face_recognition.face_encodings(image, self.locations)
            #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            for face_encoding, face_location in zip(self.encodings, self.locations):

                self.results = face_recognition.compare_faces(self.RFVmodlef.data, face_encoding, TOLERANCE)

                match = None
                if True in self.results:  # If at least one is true, get a name of first of found labels
                    self.match = self.RFVmodlef.lable[self.results.index(True)]
                    self.top_left = (face_location[3], face_location[0])
                    self.bottom_right = (face_location[1], face_location[2])

                    self.color = self.name_to_color(self.match)

                    # Paint frame
                    cv2.rectangle(image, self.top_left, self.bottom_right, self.color, FRAME_THICKNESS)

                    # Now we need smaller, filled grame below for a name
                    # This time we use bottom in both corners - to start from bottom and move 50 pixels down
                    self.top_left = (face_location[3], face_location[2])
                    self.bottom_right = (face_location[1], face_location[2] + 22)

                    # Paint frame
                    cv2.rectangle(image, self.top_left, self.bottom_right, self.color, cv2.FILLED)

                    # Wite a name
                    cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)

            return image
