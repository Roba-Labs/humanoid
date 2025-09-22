import os
import sys
from array import *
from timeit import default_timer as timer
import time

import numpy as np

sys.path.insert(1, '/home/roba/Robot_roba/scr/firmware/servo') #path init for find library
import copy

import serial.tools.list_ports
from IPython.display import clear_output

from scservo_sdk import *  # Uses SCServo SDK library

#from roba_wrist import wrist

class MOTOR_INIT:
  
    def __init__(self):
        Robaport="/dev/ttyUSB0" 
        # ports = serial.tools.list_ports.comports()
        # for port, desc, hwid in sorted(ports):
        #     if "USB-SERIAL CH340 (" +str(port) +")" ==desc:
        #        Roabport=str(port)

        #self.fist_m = wrist()
        # Control table address
        """
         forward = f
         backward = b
         left = l
         right =r
         clockwise = cw
         anti-clockwise =acw
         low = L
         high =H
         
         here low means , the lowest value from the middle value and highst value from the the middle value 
         
         1= f=L , b=H
         2= l=L , r=H
         3= cw=L , ancw=H
         4= f=L , b=H
         5= acw=L , cw=H
         6= f=L , b=H
         
         7= B=L , F=H
         8= r=L , l=H
         9= cw=L , ancw=H
         10= b=L , f=H
         11= acw=H , cw=L
         12= b=L , f=H
         
         13=
         14=
         
         
        """
        self.Motortype ={1:"sms",2:"sms",3:"sms",4:"sms",5:"scs",6:"scs",7:"sms",8:"sms",9:"sms",10:"sms",11:"scs",12:"scs",13:"scs",14:"scs"}
        self.mspeed = {1: 400, 2: 400, 3: 12, 4: 15, 5: 145, 6: 60,7: 400, 8: 400, 9: 12, 10: 12, 11: 145, 12: 145,13: 145,14: 145}
        self.joints_limit=[ [0,0,0],
         [275,60,340],[326,175,326],[180,35,355],[345,250,345], [150,80,225],[130,55,215],
         [135,70,350],[99,99,250],[215,40,360],[90,90,185],[150,80,225],[200,115,275],
         [225,134,315], [175,111,225] ]
         
        # Total lenght of angle physical (Roba robot) 
        # [ 280 ,150, 235, 95,160, 165 ]  Right hand  
        # [ 280 ,150, 355, 95,155, 160 ]  Left hand  

        # Total lenght of angle  3D webots
        #[ 270 ,205, 360, 95,240, 160 ]
        # [ [-180 ,90 ] , [-200 ,5 ]  , [-180 ,180 ] , [-95 ,0 ] , [-120 ,120 ], [-80 ,80 ] ]
        
        self.ADDR_TORQUE_ENABLE     = 40
        self.ADDR_GOAL_ACC          = 41
        self.ADDR_GOAL_POSITION     = 42  #42
        self.ADDR_GOAL_SPEED        = 46
        self.ADDR_PRESENT_POSITION  = 56
        self.ADDR_PRESENT_time      = 44

        self.MOVING_ACC                  = 0         # SCServo moving acc
        self.SCS_protocol_end            = 0         # SCServo bit end(STS/SMS=0, SCS=1)
        self.DEVICENAME                  = Robaport
        self.BAUDRATE                    = 1000000   
        # serial port init  
        self.portHandler = PortHandler(self.DEVICENAME)
        
        self.SCS_packetHandler = PacketHandler(self.SCS_protocol_end) # protocol init

        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            return 0

        #Set port baudrate
        if self.portHandler.setBaudRate(self.BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            return 0
        self.init_postion={}
        self.mID = self.LEFT_AHND_GET_ID()
        for idm in self.mID:
            self.init_postion[idm]=self.joints_limit[idm][0]
        print(self.init_postion)
        #self.LEFT_AHND_SET_POS(self.mID,self.init_postion,self.mspeed)

    # seveo set speed 
    def initmotor(self):
                self.LEFT_AHND_SET_POS(self.mID,self.init_postion,self.mspeed)
    def LEFT_AHND_SPEED( self, SCS_ID_N, SCS_MOVING_SPEED):
        self.SCS_MOVING_SPEED = SCS_MOVING_SPEED
        for SCS_ID in SCS_ID_N:
            # Write SCServo speed
            scs_comm_result, scs_error = self.SCS_packetHandler.write2ByteTxRx(self.portHandler, SCS_ID, self.ADDR_GOAL_SPEED, self.SCS_MOVING_SPEED)
            if scs_comm_result != COMM_SUCCESS:
                print("%s" % self.SCS_packetHandler.getTxRxResult(scs_comm_result))
            elif scs_error != 0:
                print("%s" % self.SCS_packetHandler.getRxPacketError(scs_error))
       
    def sms2deg(self,value):
        deg = (360*value)/4095
        return round(deg)
    def deg2sms(self,deg):
        senv = (4095*deg)/360
        return round(senv)

    def scs2deg(self,value):
        deg = (360*value)/1023
        return round(deg)
    def deg2scs(self,deg):
        senv = (1023*deg)/360
        return round(senv)
    """ 
    # servo set position 
    def SMSSM(self, SMS_ID_N , SCS_ID_N ,SCS_POSITION_VALUE1, SCS_MOVING_SPEED):

            self.SCS_MOVING_SPEED =  SCS_MOVING_SPEED
            self.SCS_POSITION_VALUE = copy.deepcopy( SCS_POSITION_VALUE1)
            SCS_packetHandler = PacketHandler(0) # protocol init
            scs_comm_result, scs_error = SCS_packetHandler.write1ByteTxRx(self.portHandler, SMS_ID_N, self.ADDR_GOAL_ACC, 0)
            scs_comm_result, scs_error = SCS_packetHandler.write2ByteTxRx(self.portHandler, SMS_ID_N, self.ADDR_GOAL_SPEED, self.SCS_MOVING_SPEED[SMS_ID_N])
            scs_comm_result, scs_error = SCS_packetHandler.write2ByteTxRx(self.portHandler, SMS_ID_N, self.ADDR_GOAL_POSITION, self.deg2sms(self.SCS_POSITION_VALUE[SMS_ID_N]))
            k=0
            l=0
            # vl =self.deg2sms(self.SCS_POSITION_VALUE[SMS_ID_N])
            # prepos = self.get_senpos(SMS_ID_N, SCS_ID_N)
            start = timer()
            while True:
                    if self.get_senpos(SMS_ID_N, SCS_ID_N)==0:
                       k=k+1
                    else:
                       k=0
                    if k==5:
                         break

            # while True:
            #     l=l+1
            #     if l==1500:
            #         break
            #     newpos=   self.get_senpos(SMS_ID_N, SCS_ID_N)
            #     if newpos == prepos:
            #        k=k+1
            #     else:
            #         k=0
            #         prepos = newpos
            #     if k==30:
            #         break
            end = timer()
            end = (end - start)*1000  
            
            return [end,k]

    def SCSSM(self, SMS_SCS_ID ,SCS_POSITION_VALUE1, SCS_MOVING_SPEED):
                

                motrsp = np.zeros(len(SMS_SCS_ID,) ,dtype=int)
                self.SCS_MOVING_SPEED = SCS_MOVING_SPEED
                self.SCS_POSITION_VALUE =SCS_POSITION_VALUE1
                # Write SCServo goal position
                SCS_packetHandler = PacketHandler(1) # protocol init
                scs_comm_result, scs_error = SCS_packetHandler.write1ByteTxRx(self.portHandler, SCS_ID_N, self.ADDR_GOAL_ACC, 0)
                scs_comm_result, scs_error = SCS_packetHandler.write2ByteTxRx(self.portHandler, SCS_ID_N, self.ADDR_GOAL_SPEED, self.SCS_MOVING_SPEED[SCS_ID_N])
                scs_comm_result, scs_error = SCS_packetHandler.write2ByteTxRx(self.portHandler, SCS_ID_N, self.ADDR_GOAL_POSITION, self.deg2scs( self.SCS_POSITION_VALUE[SCS_ID_N]))
                
                i=0
                start = timer() 
                while True:
                    i=i+1
                    if i==1000:
                        break
                    if self.get_senpos(SMS_SCS_ID)==motors_m:
                      break
            
                end = timer()
                end = (end - start)*1000 

                # prepos = self.get_senpos(SMS_ID_N, SCS_ID_N)
                # start = timer() 
                # while True:
                #     l=l+1
                #     if l==1500:
                #         break
                #     newpos=   self.get_senpos(SMS_ID_N, SCS_ID_N)
                #     if newpos == prepos:
                #       k=k+1
                #     else:
                #         k=0
                #         prepos = newpos
                #     if k==5:
                #         break
 
                
                return end,i
    """  
    
    def ReconstructAngle_left(self,deg):
        self.degs = {}
        for i in range(6):

            if i==0:
               self.degs[i+1]=self.joints_limit[i+1][0] + deg[i]
            
            elif i==1:
               self.degs[i+1]=self.joints_limit[i+1][0] + deg[i] 
            
            elif i==2:
               self.degs[i+1]=self.joints_limit[i+1][0] + deg[i]
            
            elif i==3:
               self.degs[i+1]=self.joints_limit[i+1][0] + deg[i] 

            elif i==4:
               self.degs[i+1]=self.joints_limit[i+1][0] + deg[i]
               self.degs[i+1]=self.degs[i+1]+(90-deg[2])
            
            elif i==5:
               self.degs[i+1]=self.joints_limit[i+1][0] + deg[i]

        return self.degs
    
    def ReconstructAngle_right(self,deg):
        self.degs = {}
        for i in range(7,13):

            if i==7:
               self.degs[i]=self.joints_limit[i][0] + deg[i-7]
            
            elif i==8:
               self.degs[i]=self.joints_limit[i][0]+deg[i-7]-10
            
            elif i==9:
               self.degs[i]=self.joints_limit[i][0]+deg[i-7]
            
            elif i==10:
               self.degs[i]=self.joints_limit[i][0] + deg[i-7]-15

            elif i==11:
               self.degs[i]=self.joints_limit[i][0] + deg[i-7]
               self.degs[i]=self.degs[i]-(deg[2]+90)
                    
            
            elif i==12:
               self.degs[i]=self.joints_limit[i][0] + deg[i-7]

        return self.degs
    
    def LEFT_AHND_SET_POS(self, SMS_SCS_ID, SCS_POSITION_VALUE1, SCS_MOVING_SPEED):

            motrsp = np.zeros(len(SMS_SCS_ID,) ,dtype=int)
            self.SCS_MOVING_SPEED = SCS_MOVING_SPEED
            self.SCS_POSITION_VALUE = copy.deepcopy(SCS_POSITION_VALUE1)
            motors_m=np.zeros( (len(SMS_SCS_ID),) ,dtype=int)
            
            #SCS_Servo
            for SCS_ID in SMS_SCS_ID:
                
                if self.SCS_POSITION_VALUE[SCS_ID] > self.joints_limit[SCS_ID][2] :
                    self.SCS_POSITION_VALUE[SCS_ID] = self.joints_limit[SCS_ID][2]

                elif self.SCS_POSITION_VALUE[SCS_ID] < self.joints_limit[SCS_ID][1]:
                    self.SCS_POSITION_VALUE[SCS_ID] = self.joints_limit[SCS_ID][1]

                if self.Motortype[SCS_ID]=="sms":
                    # Write SCServo speed
                    SCS_packetHandler = PacketHandler(0) # protocol init
                    scs_comm_result, scs_error = SCS_packetHandler.write1ByteTxRx(self.portHandler, SCS_ID, self.ADDR_GOAL_ACC, 0)
                    scs_comm_result, scs_error = SCS_packetHandler.write2ByteTxRx(self.portHandler, SCS_ID, self.ADDR_GOAL_SPEED, self.SCS_MOVING_SPEED[SCS_ID])
                    scs_comm_result, scs_error = SCS_packetHandler.write2ByteTxRx(self.portHandler, SCS_ID, self.ADDR_GOAL_POSITION, self.deg2sms(self.SCS_POSITION_VALUE[SCS_ID]))

                if self.Motortype[SCS_ID]=="scs":
                    # Write SCServo goal position
                    SCS_packetHandler = PacketHandler(1) # protocol init
                    scs_comm_result, scs_error = SCS_packetHandler.write1ByteTxRx(self.portHandler, SCS_ID, self.ADDR_GOAL_ACC, 0)
                    scs_comm_result, scs_error = SCS_packetHandler.write2ByteTxRx(self.portHandler, SCS_ID, self.ADDR_GOAL_SPEED, self.SCS_MOVING_SPEED[SCS_ID])
                    scs_comm_result, scs_error = SCS_packetHandler.write2ByteTxRx(self.portHandler, SCS_ID, self.ADDR_GOAL_POSITION,self.deg2scs( self.SCS_POSITION_VALUE[SCS_ID]))
            i=0
            start = time.time()
            while True:
                i=i+1
                if i==2000:
                    break
                if np.array_equal(self.get_senpos(SMS_SCS_ID),motors_m):
                   break
                
            end = time.time()
            end = (end - start)

            # start = timer() 
            # k=0
            # l=0      
            # prepos = self.LEFT_AHND_GET_POS(SMS_ID_N, SCS_ID_N, 0)
            # while True:
                
            #     l=l+1
            #     if l==1500:
            #         break
            #     newpos=   self.LEFT_AHND_GET_POS(SMS_ID_N, SCS_ID_N, 0)
            #     if newpos == prepos:
            #        k=k+1
            #     else:
            #         k=0
            #         prepos = newpos
            #     if k==5:
            #         break
            # end = timer()
            # end = (end - start)*1000   


            return end

    #get servo positopn
    
    def GET_time(self, SMS_SCS_ID ):

        self.id_position = {}
        #SMS 
         
        for SCS_ID in SMS_SCS_ID:
            if self.Motortype[SCS_ID]=="sms":
                SCS_packetHandler = PacketHandler(0) # protocol init
                scs_present_position_speed, scs_comm_result, scs_error = SCS_packetHandler.read2ByteTxRx(self.portHandler, SCS_ID,self.ADDR_PRESENT_time)
                if scs_comm_result != COMM_SUCCESS:
                    print(SCS_ID," ",self.SCS_packetHandler.getTxRxResult(scs_comm_result))
                elif scs_error != 0:
                    print(SCS_ID," ",self.SCS_packetHandler.getRxPacketError(scs_error))

                scs_present_position = SCS_LOWORD(scs_present_position_speed)
                scs_present_speed = SCS_HIWORD(scs_present_position_speed)

                self.id_position[SCS_ID] =self.sms2deg(scs_present_position)
            
        #SCS

            if self.Motortype[SCS_ID]=="scs":
                SCS_packetHandler = PacketHandler(1) # protocol init
                scs_present_position_speed, scs_comm_result, scs_error = SCS_packetHandler.read2ByteTxRx(self.portHandler, SCS_ID, self.ADDR_PRESENT_time)
                if scs_comm_result != COMM_SUCCESS:
                    print(SCS_ID," ",SCS_packetHandler.getTxRxResult(scs_comm_result))
                elif scs_error != 0:
                    print(SCS_ID," ",SCS_packetHandler.getRxPacketError(scs_error))

                scs_present_position = SCS_LOWORD(scs_present_position_speed)
                scs_present_speed = SCS_HIWORD(scs_present_position_speed)
                self.id_position[SCS_ID] =self.scs2deg( scs_present_position)
  
        #self.id_position[7]=fist

        return self.id_position
    
    def LEFT_AHND_GET_POS(self, SMS_SCS_ID ):

        self.id_position = {}
        #SMS 
         
        for SCS_ID in SMS_SCS_ID:
            if self.Motortype[SCS_ID]=="sms":
                SCS_packetHandler = PacketHandler(0) # protocol init
                scs_present_position_speed, scs_comm_result, scs_error = SCS_packetHandler.read2ByteTxRx(self.portHandler, SCS_ID, self.ADDR_PRESENT_POSITION)
                if scs_comm_result != COMM_SUCCESS:
                    print(SCS_ID," ",self.SCS_packetHandler.getTxRxResult(scs_comm_result))
                elif scs_error != 0:
                    print(SCS_ID," ",self.SCS_packetHandler.getRxPacketError(scs_error))

                scs_present_position = SCS_LOWORD(scs_present_position_speed)
                scs_present_speed = SCS_HIWORD(scs_present_position_speed)

                self.id_position[SCS_ID] =self.sms2deg(scs_present_position)
            
        #SCS

            if self.Motortype[SCS_ID]=="scs":
                SCS_packetHandler = PacketHandler(1) # protocol init
                scs_present_position_speed, scs_comm_result, scs_error = SCS_packetHandler.read2ByteTxRx(self.portHandler, SCS_ID, self.ADDR_PRESENT_POSITION)
                if scs_comm_result != COMM_SUCCESS:
                    print(SCS_ID," ",SCS_packetHandler.getTxRxResult(scs_comm_result))
                elif scs_error != 0:
                    print(SCS_ID," ",SCS_packetHandler.getRxPacketError(scs_error))

                scs_present_position = SCS_LOWORD(scs_present_position_speed)
                scs_present_speed = SCS_HIWORD(scs_present_position_speed)
                self.id_position[SCS_ID] =self.scs2deg( scs_present_position)
  
        #self.id_position[7]=fist

        return self.id_position

    def get_senpos(self, SMS_SCS_ID):
        
        motors_m=np.zeros( (len(SMS_SCS_ID),) ,dtype=int)
        i=0
        for SCS_ID in SMS_SCS_ID:
            
            #SMS 
            if self.Motortype[SCS_ID]=="sms":
                    SCS_packetHandler = PacketHandler(0) # protocol init
                    motors_m[i]=SCS_packetHandler.read1ByteTxRx(self.portHandler,SCS_ID,66)[0] 
            #SCS
            elif self.Motortype[SCS_ID]=="scs":
                    SCS_packetHandler = PacketHandler(1) # protocol init
                    motors_m[i]=SCS_packetHandler.read1ByteTxRx(self.portHandler,SCS_ID,66)[0] 
            i=i+1

        return motors_m

    def LEFT_AHND_GET_ID(self):

        ALL_ID = []
        for scsid in range(0, 15):
            try:
                scs_model_number, scs_comm_result, scs_error = self.SCS_packetHandler.ping(self.portHandler, scsid)
                if scs_comm_result == COMM_SUCCESS:
                    ALL_ID.append(scsid)
            except:
                p=0
        return ALL_ID

    def release_motors(self,SMS_SCS_ID):

        for SCS_ID in SMS_SCS_ID:
            if self.Motortype[SCS_ID]=="sms":   
                # Write SCServo speed
                SCS_packetHandler = PacketHandler(0) # protocol init
                scs_comm_result, scs_error = SCS_packetHandler.write1ByteTxRx(self.portHandler, SCS_ID, self.ADDR_TORQUE_ENABLE, 0)
                
                if scs_comm_result != COMM_SUCCESS:
                   print("%s" % self.SCS_packetHandler.getTxRxResult(scs_comm_result))
                elif scs_error != 0:
                    print("%s" % self.SCS_packetHandler.getRxPacketError(scs_error))
            if self.Motortype[SCS_ID]=="scs":
                # Write SCServo goal position
                SCS_packetHandler = PacketHandler(1) # protocol init
                scs_comm_result, scs_error = SCS_packetHandler.write1ByteTxRx(self.portHandler, SCS_ID, self.ADDR_TORQUE_ENABLE, 0)
            
                if scs_comm_result != COMM_SUCCESS:
                    print("%s" % self.SCS_packetHandler.getTxRxResult(scs_comm_result))
                elif scs_error != 0:
                    print("%s" % self.SCS_packetHandler.getRxPacketError(scs_error))

    def fist_close(self):
        #self.fist_m.close_S()
        pass
