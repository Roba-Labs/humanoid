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
            self.error=0
            self.xy=[0,0]
            self.pipeline = rs.pipeline()
            self.config = rs.config()
            self.break_loop=False
            self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
            self.pipeline_profile = self.config.resolve(self.pipeline_wrapper)
            self.device = self.pipeline_profile.get_device()

            self.found_rgb = False
            for s in self.device.sensors:
                if s.get_info(rs.camera_info.name) == 'RGB Camera':
                    self.found_rgb = True
                    break
            if not self.found_rgb:
                print("The demo requires Depth camera with Color sensor")
                exit(0)
 
            self.Weight=848
            self.Hight =480
            self.config.enable_stream(rs.stream.depth,self.Weight,self.Hight, rs.format.z16, 30)
            self.other_stream, self.other_format = rs.stream.color, rs.format.rgb8
            self.config.enable_stream(self.other_stream, self.Weight,self.Hight,self.other_format, 30)

            # Start streaming
            self.pipeline.start(self.config)
            self.profile = self.pipeline.get_active_profile()

            self.depth_profile = rs.video_stream_profile(self.profile.get_stream(rs.stream.depth))
            self.depth_intrinsics = self.depth_profile.get_intrinsics()
            self.d_weith, self.d_hight = self.depth_intrinsics.width, self.depth_intrinsics.height

            # Processing blocks
            self.pc = rs.pointcloud()
            self.decimate = rs.decimation_filter()
            self.decimate.set_option(rs.option.filter_magnitude, 2 ** 0)
            
            self.other_profile = rs.video_stream_profile(self.profile.get_stream(self.other_stream))
            self.color_intrinsics = self.other_profile.get_intrinsics()
            
                    
    
    def get_2D_3D_img(self):
        
            self.frames = self.pipeline.wait_for_frames()
  
            self.depth_frame = self.frames.get_depth_frame().as_video_frame()
            self.other_frame = self.frames.first(self.other_stream).as_video_frame()

            self.depth_frame = self.decimate.process(self.depth_frame)
           
            self.color_imag2 = np.asanyarray(self.other_frame.get_data())
            self.color_image=copy.deepcopy(self.color_imag2)
            
            self.color_image = cv2.cvtColor(self.color_image, cv2.COLOR_RGB2BGR)
            self.points = self.pc.calculate(self.depth_frame)
 
            self.verts = np.asarray(self.points.get_vertices()).reshape( self.d_hight ,self.d_weith, 3)
  

            return self.color_image , self.verts
        
    def get_2d_img_get_defth_xyz_len(self,x,y):
        
            self.frames = self.pipeline.wait_for_frames()
  
            self.depth_frame = self.frames.get_depth_frame().as_video_frame()
            self.other_frame = self.frames.first(self.other_stream).as_video_frame()

            self.depth_frame = self.decimate.process(self.depth_frame)
           
            self.color_imag2 = np.asanyarray(self.other_frame.get_data())
            self.color_image=copy.deepcopy(self.color_imag2)
            
            self.color_image = cv2.cvtColor(self.color_image, cv2.COLOR_RGB2BGR)
            self.points = self.pc.calculate(self.depth_frame)
 

            self.verts = np.asarray(self.points.get_vertices()).reshape( self.d_hight ,self.d_weith, 3)
            
            # self.xx=int((848*x)/1280)
            # self.yy=int( (480*y)/720)  
            self.xx= x 
            self.yy= y 
            
            if x> 846:
                 self.xx=847
                        
            if y > 479:
                 self.yy=479
                        
            self.xyz=np.around(self.verts[self.yy,self.xx],3) 

            return self.color_image , [self.xyz[0],self.xyz[1],self.xyz[2]] ,self.verts

    
    def mouse_cb1(self,event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            self.xy[0]=x
            self.xy[1]=y
            
    def dispalym(self,img):
        
                cv2.namedWindow("roba robot", cv2.WINDOW_NORMAL)
                cv2.imshow("roba robot",  img)
                
                key = cv2.waitKey(1)
                if key in (27, ord("q")) or cv2.getWindowProperty("roba robot", cv2.WINDOW_NORMAL) < 0:
                    self.break_loop=True
                    cv2.destroyAllWindows()
                    
                     
    def  display_all_set_p(self,color_image3 ,xyz1):

                cv2.namedWindow("roba robot", cv2.WINDOW_NORMAL)
                cv2.setMouseCallback("roba robot", self.mouse_cb1)

            #try:
                xx=copy.deepcopy(self.xy[0])
                yy =copy.deepcopy(self.xy[1])
              
                self.error=self.error+1
               
                self.txtl="X="+str(xyz1[0])+" , Y="+str(xyz1[1])+", Z="+str(xyz1[2])
                
                cv2.putText(color_image3 ,self.txtl , (20, color_image3.shape[0]-20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 
                            thickness=2, lineType=cv2.LINE_AA)
                            
                cv2.putText(color_image3 , f"X={self.xy[0] } Y={self.xy[1]}", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 
                        thickness=2, lineType=cv2.LINE_AA)

                cv2.line(color_image3, (10,360),(color_image3.shape[1]-10 ,360), (0,0,255), 2)
                cv2.line(color_image3, (640,10),(640 ,color_image3.shape[0]-10), (0,0,255), 2)

                cv2.namedWindow("roba robot", cv2.WINDOW_NORMAL)
                cv2.imshow("roba robot",  color_image3)
                
                key = cv2.waitKey(1)
                if key in (27, ord("q")) or cv2.getWindowProperty("roba robot", cv2.WINDOW_NORMAL) < 0:
                    self.break_loop=True
                    cv2.destroyAllWindows()
                     
            # except:
            #   print("error",self.error)
            #   if self.error==100:
            #         self.break_loop=True
   
    def clean_cam(self):
        self.pipeline.stop()
    
    def display_all(self):

        cv2.namedWindow("roba robot", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("roba robot", self.mouse_cb1)

        while True:
            #try:
               
  
                xx=copy.deepcopy(self.xy[0])
                yy =copy.deepcopy(self.xy[1])
             
                        
                self.color_image3 ,self.xyz1,self.verts = self.get_2d_img_get_defth_xyz_len(self.xy[0],self.xy[1])
                clear_output(True)
                print(self.color_image3.shape)
                self.txtl="X="+str(self.xyz1[0])+" , Y="+str(self.xyz1[1])+", Z="+str(self.xyz1[2])
                
                cv2.putText(self.color_image3 , f"X={self.xy[0] } Y={self.xy[1]}", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 
                        thickness=2, lineType=cv2.LINE_AA)

                cv2.putText(self.color_image3 ,self.txtl , (20, self.color_image3.shape[0]-20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 
                            thickness=2, lineType=cv2.LINE_AA)

                cv2.line(self.color_image3, (10,360),(self.color_image3.shape[1]-10 ,360), (0,0,255), 2)
                cv2.line(self.color_image3, (640,10),(640 ,self.color_image3.shape[0]-10), (0,0,255), 2)

                cv2.namedWindow("roba robot", cv2.WINDOW_NORMAL)
                cv2.imshow("roba robot",  self.color_image3)
                
                key = cv2.waitKey(1)
                if key in (27, ord("q")) or cv2.getWindowProperty("roba robot", cv2.WINDOW_NORMAL) < 0:
                    cv2.destroyAllWindows()
                    break  
            # except:
            #   self.pipeline.stop()
            #   cv2.destroyAllWindows()
            #   pass
        self.pipeline.stop()
           