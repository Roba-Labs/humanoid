from IPython.display import clear_output
import time
from camera3D2 import Camera_3D
from face_detection import Roba_Faces_recognition
import os
import numpy as np
import copy
from threading import Thread 
roba_cam = Camera_3D()
time.sleep(0.5)
satr = time.time()
break_loop=True
def img_pos_cal1():
    c=0
    try:
        #for f in range(300):
        while True:
                clear_output(True)
                #print("start")
                img,ver,boxs= roba_cam.get_2D_3D_img_pos(0)
                if time.time() - satr >10:
                    break
                #print(" end ")
                #img,ver,vrte =roba_cam.get_2d_img_get_defth_xyz_len(roba_cam.xy[0],roba_cam.xy[1])
                #lebal , xyzp,hw,obs=objtrack.get_only_xyz_len(img,ver,boxs)
                #roba_cam.display_all_set_p(img,ver)
                #roba_cam.dispalym(img)
                #roba_cam.display_all()
                c=c+1
                #print(lebal)
                #print(xyzp)
                #print(hw)
                #print(obs)
                #print(c)
                #print(" end ")
                #time.sleep(0.05)
                #if  break_loop:
                #    print("break")
                #    break
        # print("break 2 ")
        # roba_cam.break_loop=True
        # img,ver,boxs= roba_cam.get_2D_3D_img_pos(1)
    finally:
        print("All break 2 ")
    print("All break  ")
    roba_cam.pipeline.stop()
    
img_pos_cal1()   