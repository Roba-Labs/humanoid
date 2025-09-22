import sys
import smbus2 as smbus 
import time
import Jetson.GPIO as GPIO
import time

class Fingers:
    def __init__(self):
         self.I2C_SLAVE_ADDRESS = 8 #0x0b ou 11
         self.I2Cbus = smbus.SMBus(1)
        
    def Mpower_off(self):
        self.I2Cbus.write_byte_data(8, 2,1)
        
    def send(self,data):
        self.I2Cbus.write_byte_data(8, 2,data)
        
    def LF_close(self):
        for i in range(10,15):
            if i%2==0:
               self.I2Cbus.write_byte_data(8, 2,i)
               time.sleep(0.02)
        time.sleep(1.5)
        self.I2Cbus.write_byte_data(8, 2,16)
        
    def LF_open(self):
        self.I2Cbus.write_byte_data(8, 2,17)
        time.sleep(0.5)
        for i in range(11,16):
            if i%2==1:
               self.I2Cbus.write_byte_data(8, 2,i)
               time.sleep(0.02)
        time.sleep(1.7)
        self.I2Cbus.write_byte_data(8, 2,1)
        
    def RF_close(self):
        for i in range(2,7):
            if i%2==0:
               self.I2Cbus.write_byte_data(8, 2,i)
               time.sleep(0.02)
        time.sleep(1.5)
        self.I2Cbus.write_byte_data(8, 2,8)
        
    def RF_open(self):
        self.I2Cbus.write_byte_data(8, 2,9)
        time.sleep(0.5)
        for i in range(3,8):
            if i%2==1:
               self.I2Cbus.write_byte_data(8, 2,i)
               time.sleep(0.02)
        time.sleep(1.7)
        self.I2Cbus.write_byte_data(8, 2,1)

    def closbus(self):
        self.I2Cbus.close()