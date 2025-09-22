
import time

import serial

from wrist_enum import fingers


class wrist:
      
        def __init__(self):
            self.roba_connection = serial.Serial()
            self.roba_connection.baudrate = 115200
            self.roba_connection.port = 'COM12'
            self.roba_connection.timeout = 0.1
            self.roba_connection.open()
            self.Fingers = fingers()
            self.lastdata=''
            time.sleep(1)
        # send data to ardiuno
        def send_data(self,data):
            if (self.roba_connection.is_open):
                
                self.roba_connection.write(data.encode())
                while True:
                    v = self.roba_connection.readline().decode()
                    if v != "":
                        self.lastdata=v
                        #print(v)
                        break
        # read data from arduino
        def read_all(self):
             if (self.roba_connection.is_open):
                 return self.roba_connection.readline().decode()
       
        def send_datatf(self,data):
            if (self.roba_connection.is_open):
                self.roba_connection.write(data.encode())
                #
                # while True:
                #     v = self.roba_connection.readline().decode()
                #     if v != "":
                #         self.lastdata=v
                #         #print(v)
                #         break

        def finger1_forward(self):
            if (self.roba_connection.is_open):
                data = self.Fingers.write + self.Fingers.write_store + self.Fingers.finger1 + self.Fingers.finger_condition0 + self.Fingers.finger_condition1
                self.send_data(data)
                #print(data)

        def finger1_backwoard(self):
            if (self.roba_connection.is_open):
                data = self.Fingers.write + self.Fingers.write_store+ self.Fingers.finger1 + self.Fingers.finger_condition1 + self.Fingers.finger_condition0
                self.send_data(data)
                #print(data)

        def finger1_reset(self): 
            if (self.roba_connection.is_open):
                data = self.Fingers.write + self.Fingers.write_store + self.Fingers.finger1 + self.Fingers.finger_condition0 + self.Fingers.finger_condition0
                self.send_data(data)
                #print(data)


        def finger2_forward(self):
            if (self.roba_connection.is_open):
                data = self.Fingers.write + self.Fingers.write_store + self.Fingers.finger2 + self.Fingers.finger_condition0 + self.Fingers.finger_condition1
                self.send_data(data)
                #print(data)

        def finger2_backwoard(self):
            if (self.roba_connection.is_open):
                data = self.Fingers.write + self.Fingers.write_store+ self.Fingers.finger2 + self.Fingers.finger_condition1 + self.Fingers.finger_condition0
                self.send_data(data)
                #print(data)

        def finger2_reset(self): 
            if (self.roba_connection.is_open):
                data = self.Fingers.write + self.Fingers.write_store + self.Fingers.finger2 + self.Fingers.finger_condition0 + self.Fingers.finger_condition0
                self.send_data(data)
                #print(data)


        def finger3_forward(self):
            if (self.roba_connection.is_open):
                data = self.Fingers.write + self.Fingers.write_store + self.Fingers.finger3 + self.Fingers.finger_condition1 + self.Fingers.finger_condition0 
                self.send_data(data)
                #print(data)

        def finger3_backwoard(self):
            if (self.roba_connection.is_open):
                data = self.Fingers.write + self.Fingers.write_store+ self.Fingers.finger3  + self.Fingers.finger_condition0 + self.Fingers.finger_condition1
                self.send_data(data)
                #print(data)

        def finger3_reset(self): 
            if (self.roba_connection.is_open):
                data = self.Fingers.write + self.Fingers.write_store + self.Fingers.finger3 + self.Fingers.finger_condition0 + self.Fingers.finger_condition0
                self.send_data(data)
                #print(data)



        def finger4_forward(self):
            if (self.roba_connection.is_open):
                data = self.Fingers.write + self.Fingers.write_store + self.Fingers.finger4  + self.Fingers.finger_condition1+ self.Fingers.finger_condition0
                self.send_data(data)
                #print(data)

        def finger4_backwoard(self):
            if (self.roba_connection.is_open):
                data = self.Fingers.write + self.Fingers.write_store+ self.Fingers.finger4+ self.Fingers.finger_condition0 + self.Fingers.finger_condition1 
                self.send_data(data)
                #print(data)

        def finger4_reset(self): 
            if (self.roba_connection.is_open):
                data = self.Fingers.write + self.Fingers.write_store + self.Fingers.finger4 + self.Fingers.finger_condition0 + self.Fingers.finger_condition0
                self.send_data(data)
                #print(data)


        def fist(self):
            self.finger2_forward()
            self.finger3_forward()
            self.finger4_forward()
            self.fingers_action()
            time.sleep(2.5)
            self.finger1_forward()
            self.fingers_action()
        
        def unfist(self):
            self.finger1_backwoard()
            self.fingers_action()
            time.sleep(1.1)
            self.finger2_backwoard()
            self.finger3_backwoard()
            self.finger4_backwoard()
            self.fingers_action()
            time.sleep(2)
            self.finger1_reset()
            self.finger2_reset()
            self.finger3_reset()
            self.finger4_reset()
            self.fingers_action()
        
        def clean_fist(self):
            self.finger1_reset()
            self.finger2_reset()
            self.finger3_reset()
            self.finger4_reset()
            self.fingers_action()

        def fingers_action(self):
            if (self.roba_connection.is_open):
                data = self.Fingers.write + self.Fingers.write_action 
                self.send_data(data)
                #print(data)
              
        def resetAll(self):
            if (self.roba_connection.is_open):
                 data ="3"
                 self.send_data(data)
                 #print(data)

        def close_S(self):
            self.roba_connection.close()

        




