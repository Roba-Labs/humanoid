#!/usr/bin/python3
import sys
 
sys.path.insert(1, '/home/roba/Robot_roba/scr/Robamain')  
sys.path.insert(1, '/home/roba/Robot_roba/scr/Roba_conversion_ai')  
sys.path.insert(1, '/home/roba/Robot_roba/scr/Roba_vision')  
sys.path.insert(1, '/home/roba/Robot_roba/scr/firmware/servo')  

import ASR
import robaaibot
import threading
import time
import Speak2rpi

from robalimbs import Limbs
import pickle
import numpy as np
from motor_init import MOTOR_INIT
from roba_record import Roba_recoddata
from wristfingers import Fingers
import smbus2 as smbus 
import time
import Jetson.GPIO as GPIO
import tracking
from camera3D2 import Camera_3D
from IPython.display import clear_output
class app:
       
        def __init__(self,name):
                
            self.name=name
            self.limbs=np.array([])
            self.CAIb=True     
                
        def chat2(self):
                self.robachatbot = robaaibot.RobaBot()
                time.sleep(0.2)
                self.spk = Speak2rpi.speak("192.168.0.120")
                time.sleep(0.5)
                self.spk.recev_data="Paused"
                
        def init_CAI(self):
            playtim=0
            self.asrs = ASR.ASRtext()
            global anstext
            while self.CAIb:
                    textq=""
                    time.sleep(0.2)

                    if self.spk.recev_data=="Paused":
                        playtim=0
                        textq = self.asrs.get_text()
                        
                        if textq =='' and textq ==" ":   
                            
                            textq="&"
                            self.asrs.clear_text()
                            self.asrs.microph=True
                            
                        if textq !="&" and len(textq)>1 and textq != "['']" and textq !='' and textq !=" ":
                           self.asrs.clear_text()
                           #clear_output(True)
                           print(textq)
                           anstext= self.robachatbot.get_ans(textq) 
                           textq="&"
                           anstext = str(anstext)
                           if len(anstext)>1 and anstext != "['']" and anstext !='' and anstext !=" ":                                       
                                self.spk.Speaking(anstext)
                                start_time = time.time()
                                
                                while self.spk.recev_data !="Playing":
                                        time.sleep(0.1)
                                        self.asrs.clear_text()
                                        if  time.time() - start_time>5:
                                            break
                                start_time = time.time()
                                while self.spk.recev_data !="Paused":
                                        self.asrs.microph=False
                                        self.asrs.clear_text()
                                        time.sleep(0.1)
                                        if  time.time() - start_time>50:
                                            break
                                self.asrs.microph=True
                                time.sleep(1.3)
                                self.asrs.clear_text()
                                
                        else:
                           self.asrs.microph=True
                           self.asrs.clear_text()
                           

            print("exit CAI")
        
        def chat(self):
                self.CAIb=True
                CAIT  =  threading.Thread(target= self.init_CAI,daemon=True) 
                CAIT.start()

        def initlimbs(self,limbnames):
               
                if limbnames=="handhead":
                        self.smotor = MOTOR_INIT()   
                        self.ID = self.smotor.LEFT_AHND_GET_ID()
                if limbnames=="handheadstore":
                        self.handsheaddata=Roba_recoddata(self.smotor.init_postion)
                if limbnames=="fingers":
                        self.finger = Fingers()
                        
                if limbnames=="tracker":
                        self.track = tracking.Track()
                        for i in range(5):
                           clear_output(True)
                           print(self.track.RPY)
                           print(self.track.trans)
                           time.sleep(0.1) 
                if limbnames=="vision":
                        self.roba_cam = Camera_3D()
                        time.sleep(1) 
                
                if limbnames=="chat":
                        self.chat()
                        self.chat2()
                        
        def initlimb(self):
                for name in self.limbs:
                        self.initlimbs(name)
                        
        def addlimb(self,limbname):
            self.limbs=np.append(self.limbs,limbname)
            self.initlimbs(limbname)
                
        def righthandpos(self):
                 motors_p = self.smotor.LEFT_AHND_GET_POS(self.ID[0:7])
                 motors_s={}
                 for i in range(1,8):
                     motors_s[i]=self.smotor.smotor[i]
                 return [motors_p , motors_s]
                
        def lefthandpos(self):
                 motors_p = self.smotor.LEFT_AHND_GET_POS(self.ID[7:13])
                 motors_s={}
                 for i in range(7,13):
                     motors_s[i]=self.smotor.smotor[i]
                 return [motors_p , motors_s]
                
        def headpos(self):
                 motors_p = self.smotor.LEFT_AHND_GET_POS(self.ID[13:15])
                 motors_s={}
                 for i in range(13,15):
                     motors_s[i]=self.smotor.mspeed[i]
                 return [motors_p , motors_s]
                
        def servoespos(self,key):
                motors_p = self.smotor.LEFT_AHND_GET_POS(key)
                return motors_p
        
        def allsspos(self):
                motors_p = self.smotor.LEFT_AHND_GET_POS(self.ID)
                return [motors_p,self.smotor.mspeed]
        
        def smotorinit(self):
                self.smotor.LEFT_AHND_SET_POS(self.smotor.mID,self.smotor.init_postion,self.smotor.mspeed)
                
        def getruntimelimb(self,name,key):
                
                if name=="righthand":
                        if key=="readpos":
                             return  self.righthandpos()
                if name=="lefthand":
                        if key=="readpos":
                             return  self.lefthandpos()
                if name=="head":
                        if key=="readpos":
                             return  self.headpos()
                if name=="allservo":
                        if key=="readpos":
                            return  self.allsspos()
                if name=="servoespos":
                            return   self.servoespos(key)
                if name=="handreleaseall":
                        self.smotor.release_motors(self.ID)
                if name=="handrelease":
                        self.smotor.release_motors(key)
                        
                if name=="handinit":
                        self.smotorinit()
                        
                if name=="rightfinger":
                        if key=="open":
                             self.finger.RF_open()  
                if name=="rightfinger":
                        if key=="close":
                             self.finger.RF_close()
                if name=="leftfinger":
                        if key== "open":
                             self.finger.LF_open()
                if name=="leftfinger":
                        if key=="close":
                             self.finger.LF_close()
                if name=="fingeroff":
                             self.finger.Mpower_off()
                if name=="fingersopncl":
                     for k in  key:
                        self.finger.send(k)
                        time.sleep(0.02)
                        
                if name=="tracker":
                       if key=="rpy":
                          return self.track.RPY
                if name=="tracker":
                       if key=="trans":
                          return self.track.trans
                        
                if name=="vision":
                       if key=="0":
                           img,ver,boxs= self.roba_cam.get_2D_3D_img_pos(0)
                           return [img,ver,boxs]
                       else:
                          img,ver,boxs= self.roba_cam.get_2D_3D_img_pos(1)
                          return [img,ver,boxs]
                return 0
        
        
        
        def addrighthand(self,data):
             self.handhead.append(data)
                
        def addlimdata(self,limbname,data):   
                if limbname=="handhead":
                        self.addrighthand(data)

class Roba:
    def __init__(self):
        
        self.limbslist=Limbs().lims.tolist()
        self.apps={}
        
    def creatapp(self,name):
        self.apps[name]=app(name)
    
    def appslist(self):
                self.app=np.array([])
                for apk in self.apps:
                        self.app = np.append(self.app,[apk]) 
                self.app=self.app.tolist() 
                return self.app
        
    def appruntimedata(self,appname,limb,key):
            apps = self.apps[appname]
            appdatas = apps.getruntimelimb(limb,key)
            
            return appdatas
                
    def appaddlims(self,appname,limbname):
        apps = self.apps[appname]
        apps.addlimb(limbname)
        
    def appinitlims(self,appname):
        apps = self.apps[appname]
        apps.addlimb()
        
    def appinfo(self,name):
        apps = self.apps[name]
        print("..........app limbs.........")
        print(" ")
        print(apps.limbs.tolist())
        print(" ")
        
    def appofflimbs(self,appname,limbname):
                apps = self.apps[appname]
                if limbname=="handhead":
                        apps.smotor.portHandler.closePort()
                        apps.smotor.fist_close()   
                if limbname=="handheadstore":
                        self.handsheaddata=None
                if limbname=="fingers":
                        apps.finger.I2Cbus.close() 
                if limbname=="tracker":
                        apps.track.break_loop=False  
                if limbname=="vison":
                        apps.roba_cam.break_loop=False
                        apps.roba_cam.pipeline.stop()
                if limbname=="chat":
                        apps.CAIb=False       
             
# def main():
#     rb=Roba()
#     print(rb.limbslist)
    
# if __name__ == "__main__":
#     main()
# appname=name+".rap"
#        with open(appname, 'wb') as roba_face_model:
#             pickle.dump(robaapp, roba_face_model)