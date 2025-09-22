import copy
import ctypes
import math
from IPython.display import clear_output
import cv2
import numpy as np
import pyrealsense2 as rs

class Camera_3D:

    def __init__(self):
                    
            # Configure streams
 
            self.W=848
            self.H =480
            self.break_loop=False

            # Configure depth and color streams
            self.pipeline = rs.pipeline()
            self.config = rs.config()
            

            self.config.enable_stream(rs.stream.depth, self.W,self.H , rs.format.z16, 30)
            self.config.enable_stream(rs.stream.color ,self.W,self.H , rs.format.bgr8, 30)

            self.pipeline.start(self.config)
   
            self.aligned_stream = rs.align(rs.stream.color) # alignment between color and depth
            self.point_cloud = rs.pointcloud()
            # self.pipeline.stop()
                    
    
    def get_2D_3D_img(self):
        
              # Capture frame-by-frame
            frames =  self.pipeline.wait_for_frames()
            frames =  self.aligned_stream.process(frames)
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame().as_depth_frame()

            points =  self.point_cloud.calculate(depth_frame)
            verts = np.asanyarray(points.get_vertices()).view(np.float32).reshape(-1, self.W, 3)  # xyz
            #verts= verts 
            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            # skip empty frames
            
            #print("[INFO] found a valid depth frame")
            color_image = np.asanyarray(color_frame.get_data())
            image =copy.deepcopy(color_image)
   
            
            return image , verts
        
    
    def dispalym(self,img):
        
                cv2.namedWindow("roba robot", cv2.WINDOW_NORMAL)
                cv2.imshow("roba robot",  img)
                
                key = cv2.waitKey(1)
                if key in (27, ord("q")) or cv2.getWindowProperty("roba robot", cv2.WINDOW_NORMAL) < 0:
                    self.break_loop=True
                    cv2.destroyAllWindows()
           