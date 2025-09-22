import copy
import math as m
import time
from threading import Thread

import numpy as np
import pyrealsense2 as rs
from IPython.display import clear_output


# Declare RealSense pipeline, encapsulating the actual device and sensors
class Track:
           
    def gyro_data(self,gyro):
        return np.asarray([gyro.x, gyro.y, gyro.z])
    def accel_data(self,accel):
        return np.asarray([accel.x, accel.y, accel.z])  

    def img_pos_cal(self):
        #try:
            while (self.break_loop):
                # Wait for the next set of frames from the camera
                frames = self.pipe.wait_for_frames()
                pose = frames.get_pose_frame()

               
                if pose:
                    # Print some of the pose data to the terminal
                    data = pose.get_pose_data()
                    X = data.translation.x
                    Y = data.translation.y
                    Z = data.translation.z
                    
                    w = data.rotation.w
                    x = -data.rotation.z
                    y = data.rotation.x
                    z = -data.rotation.y
                    #clear_output(True)
                    pitch =  -m.asin(2.0 * (x*z - w*y)) * 180.0 / m.pi;
                    roll  =  m.atan2(2.0 * (w*x + y*z), w*w - x*x - y*y + z*z) * 180.0 / m.pi;
                    yaw   =  m.atan2(2.0 * (w*z + x*y), w*w + x*x - y*y - z*z) * 180.0 / m.pi;
                    self.RPY =copy.deepcopy([pitch,roll,yaw]) # pitch=x,roll=y,yaw=z
                    xyz = np.round_([X,Y,Z],3)
                    xyz=xyz*100
                    self.trans=copy.deepcopy(xyz)
                     
            self.pipe.stop()
            print("stop")
    def __init__(self):
         
        self.pipe = rs.pipeline()

        # Build config object and request pose data
        self.cfg = rs.config()
        self.cfg.enable_stream(rs.stream.pose)
        # self.cfg.enable_stream(rs.stream.accel)
        # self.cfg.enable_stream(rs.stream.gyro)
        # Start streaming with requested config
        self.pipe.start(self.cfg)
        self.gytts=0
        self.cnt=0
        self.cnt1=0
        self.degree=[]
        self.accl=[]
        self.erorac=[10,10,10]
        self.break_loop=True
        self.RPY=[0,0,0]
        self.accel=[]
        self.gyr_rpy=[]
        self.trans=[]
        time.sleep(0.5)
        self.th = Thread(target=self.img_pos_cal)
        self.th.start()
 

# track = Track()
# track.accl=[0,0,0]
# #for i in range(1000):
# while(True):
#     clear_output(True)
#     time.sleep(0.01)
#     print(track.RPY)
# #    print(track.accel)
# #    print(track.accl)
#     print(track.trans)
#     print(" ")
#     print(" ")

# track.break_loop=False
# track.pipe.stop()

"""
                accel = self.accel_data(frames[1].as_motion_frame().get_motion_data())
                self.accel=copy.deepcopy(accel)
                # self.accl.append(accel)
                # if self.cnt==15:
                #     self.cnt=0
                #     self.accl=[]
                self.accl=[0,0,0]
                ack =np.round_( np.subtract(self.erorac ,accel), decimals = 1) 
                for cks in ack:
                    if cks==0:
                        self.cnt=0
                    else:
                        self.cnt=self.cnt+1
                    
                if self.cnt>=2:
                    self.accl=ack
                    self.cnt1=0
                else:
                   self.cnt1=self.cnt1+1
                if self.cnt1==15:
                    self.cnt1=0
                    self.accl=[]
                
                # gyrof =  frames[2].as_motion_frame()
                # #self.gytts=gyrof.get_timestamp()
                # gyro = self.gyro_data(gyrof.get_motion_data())
                # self.gyr_rpy=copy.deepcopy(gyro)
                
                # Fetch pose frame
                self.erorac=accel
"""