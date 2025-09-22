import copy
import ctypes
import math
from IPython.display import clear_output
import cv2
import numpy as np
import pyrealsense2 as rs
import time
from tracker import *
import imutils
class Camera_3D:

    def __init__(self):
            
            # Configure streams
            self.W=848
            self.H =480
            self.xy=[0,0]
            self.break_loop=False

            # Configure depth and color streams
            self.gytts=0
            self.cnt=0
            self.cnt1=0
            self.degree=[]
            self.accl=[]
            self.erorac=[10,10,10]
            self.pipeline = rs.pipeline()
            self.config = rs.config()
            self.tracker = EuclideanDistTracker()
            self.object_detector = cv2.createBackgroundSubtractorMOG2(history = 500, varThreshold = 30)
            # self.config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 250)
            # self.config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)
            # self.config.enable_stream(rs.stream.accel)
            # self.config.enable_stream(rs.stream.gyro)
            self.config.enable_stream(rs.stream.depth, self.W,self.H , rs.format.z16, 30)
            self.config.enable_stream(rs.stream.color ,self.W,self.H , rs.format.bgr8, 30)
            #self.config.enable_record_to_file('test.bag')
            self.pipeline.start(self.config)
            self.aligned_stream = rs.align(rs.stream.color)  
            self.point_cloud = rs.pointcloud()
            
    def gyro_data(self,gyro):
        return np.asarray([gyro.x, gyro.y, gyro.z])
    def accel_data(self,accel):
        return np.asarray([accel.x, accel.y, accel.z])  
    def display_2d_3d_(self,color_image,depth_image):
        

                roi2 = color_image[10:470,284:564] #[10,470,284,564]
               
                gray = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
                th, threshed = cv2.threshold(gray,100,100, cv2.THRESH_BINARY_INV) #240, 255
                ## (2) Morph-op to remove noise
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
                morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)
                ## (3) Find the max-area contour
                cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                detections = []
                for cnt in cnts:
                    # Calculate area and remove small elements
                    #cnt = sorted(cnts, key=cv2.contourArea)[-1]
                    area = cv2.contourArea(cnt)
                    if area >150:
                        #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                        x, y, w, h = cv2.boundingRect(cnt)

                        detections.append([284+x, y,284+x + w, y + h])
                
                for box_id in detections:
                    x, y, w, h = box_id
                    cv2.rectangle(color_image, (x, y), (x + w, y + h), (0,0, 255), 3)
 
#                 print(len(detections))
#                 if self.break_loop:
#                     time.sleep(1)
#                     cv2.destroyAllWindows()
#                 else:
#                     cv2.imshow("roba robot", color_image)
#                     cv2.imshow("roba threshed", threshed)
#                     cv2.imshow('Canny Edge Detection', edges)
#                     #cv2.imshow("roba robot", images)
#                     if cv2.waitKey(1) & 0xFF == ord('q'):
#                         self.break_loop=True
#                         #cv2.destroyAllWindows()
                           
                # except:
                #    pass
                return detections                
                
    def display_2d_3d_2(self,color_image,depth_image):
        
               

                roi = color_image[10:470,284:564] #[10,470,284,564]
                
                img_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                # Blur the image for better edge detection
                img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
                edges = cv2.Canny(image=img_blur, threshold1=70, threshold2=70) # Canny Edge Detection
                
                mask = self.object_detector.apply(roi)
                _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                detections = []
                #try:
                for cnt in contours:
                    # Calculate area and remove small elements
                    area = cv2.contourArea(cnt)
                    if area > 100:
                        #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                        x, y, w, h = cv2.boundingRect(cnt)

                        detections.append([x, y, w, h])

                # 2. Object Tracking
                boxes_ids = self.tracker.update(detections)
                for box_id in boxes_ids:
                    x, y, w, h, id = box_id
                    cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
                #images = np.hstack((color_image, roi))
                cv2.rectangle(color_image, (284, 10), (564,470), (0, 255, 0), 3)
                if self.break_loop:
                    time.sleep(1)
                    cv2.destroyAllWindows()
                else:
                    cv2.imshow("roba robot mask", mask)
                    cv2.imshow("roba robot", color_image)
                    cv2.imshow('Canny Edge Detection', edges)
                    #cv2.imshow("roba robot", images)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.break_loop=True
                        #cv2.destroyAllWindows()
                           
                # except:
                #    pass
   
        
    def display_2d_3d_1(self,color_image,depth_image):
             
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
                obstacle=[340,470,350,564] 
                depth_colormap = cv2.rectangle(depth_colormap, (obstacle[2],obstacle[0]), (obstacle[3],obstacle[1]), (0, 0, 255), 2)
                color_image = cv2.rectangle(color_image, (obstacle[2],obstacle[0]), (obstacle[3],obstacle[1]), (0,0, 255), 2)
                
                depth_colormap_dim = depth_colormap.shape
                color_colormap_dim = color_image.shape
                
                
        # If depth and color resolutions are different, resize color image to match depth image for display
                if depth_colormap_dim != color_colormap_dim:
                    resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
                    images = np.hstack((resized_color_image, depth_colormap))
                else:
                    images = np.hstack((color_image, depth_colormap))

                # Show images
                if self.break_loop:
                    time.sleep(1)
                    cv2.destroyAllWindows()
                else:
                    cv2.namedWindow("roba robot", cv2.WINDOW_NORMAL)
                    cv2.imshow("roba robot", images)
                    key = cv2.waitKey(1)
                    if key in (27, ord("q")) or cv2.getWindowProperty("roba robot", cv2.WINDOW_NORMAL) < 0:
                        self.break_loop=True
                        cv2.destroyAllWindows()
        
    def get_2D_3D_img_pos(self,p=0):
        
            frames =  self.pipeline.wait_for_frames()
            frames =  self.aligned_stream.process(frames)
                    
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame().as_depth_frame()

            points =  self.point_cloud.calculate(depth_frame)
            verts = np.asanyarray(points.get_vertices()).view(np.float32).reshape(-1, self.W, 3)  # xyz
  
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
             
            image =copy.deepcopy(color_image)
            boxs=[]
            if p==1:
                boxs=self.display_2d_3d_(color_image,depth_image)
            return color_image,verts,boxs ,depth_image
        
    def get_2d_img_get_defth_xyz_len(self,x,y):
        
              # Capture frame-by-frame
            frames =  self.pipeline.wait_for_frames()
            frames =  self.aligned_stream.process(frames)
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame().as_depth_frame()

            points =  self.point_cloud.calculate(depth_frame)
            verts = np.asanyarray(points.get_vertices()).view(np.float32).reshape(-1, self.W, 3)  # xyz
            #verts= verts 
            # Convert images to numpy arrays
            #print(verts.shape)
            depth_image = np.asanyarray(depth_frame.get_data())
            # skip empty frames
            
            #print("[INFO] found a valid depth frame")
            color_image = np.asanyarray(color_frame.get_data())
            image =copy.deepcopy(color_image)
            #return verts 
            # self.xx=int((848*x)/1280)
            # self.yy=int( (480*y)/720)  
            xx= x 
            yy= y 
            
            if xx > 846:
                xx=847
                        
            if yy > 479:
                yy=479
                        
            self.xyz=np.around(  verts[yy,xx]*100 , decimals=3)  

            return image , [self.xyz[0],self.xyz[1],self.xyz[2]]

    
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
                    
    
   
    def display_all(self):
        cv2.namedWindow("roba robot", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("roba robot", self.mouse_cb1)

        while True:
            #try:
               
                xx=copy.deepcopy(self.xy[0])
                yy =copy.deepcopy(self.xy[1])
                
                self.color_image3, self.xyz1  = self.get_2d_img_get_defth_xyz_len(self.xy[0],self.xy[1])
                # clear_output(True)
                # print(self.color_image3.shape)
                self.txtl="X="+str(self.xyz1[0])+" , Y="+str(self.xyz1[1])+", Z="+str(self.xyz1[2])
                self.txtl2="X="+str(self.xyz1[0])+" , Y="+str(-self.xyz1[1])+", Z="+str(self.xyz1[2])
                
                cv2.putText(self.color_image3 , f"X={xx} Y={yy}", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 
                        thickness=2, lineType=cv2.LINE_AA)

                cv2.putText(self.color_image3 ,self.txtl , (20, self.color_image3.shape[0]-20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 
                            thickness=2, lineType=cv2.LINE_AA)
                
                cv2.putText(self.color_image3 ,self.txtl2 , (20, self.color_image3.shape[0]-40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 
                            thickness=2, lineType=cv2.LINE_AA)

                cv2.line(self.color_image3, (10,int(self.H/2)),(self.color_image3.shape[1]-10 ,int(self.H/2)), (0,0,255), 2)
                cv2.line(self.color_image3, (int(self.W/2),10),(int(self.W/2) ,self.color_image3.shape[0]-10), (0,0,255), 2)

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
           