import torch
import os
import cv2
import numpy as np
import copy
#os.chdir( '/home/roba/Robot_roba')

class track_obj:
    def __init__(self):
          #self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='./libs/yolov5s.pt', force_reload=True).autoshape()
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s') 
   
    def get_boxs_img_xyzc(self,image,verts):
            image2 = copy.deepcopy(image)
            imgsbox = self.model(image).pandas().xyxy[0]
             
            labels = imgsbox['name']
            xmin =  imgsbox['xmin']
            ymin =  imgsbox['ymin']
            xmax =  imgsbox['xmax']
            ymax =  imgsbox['ymax']
            conf = imgsbox["confidence"]
            cngp=False
            nobj=0
            obj_l=[]
            for i in range(len(labels)):
                if round(conf[i] ,3)>0.50:
                    if labels[i]=='__background__' or labels[i]== 'bottle':
                    # if labels[i]=='__background__' or labels[i]== 'person' or labels[i]=='handbag' or labels[i]=='tie'  or labels[i]=='suitcase' or labels[i]=='sports ball' or labels[i]=='baseball bat' or labels[i]=='bottle' or labels[i]=='cup' or labels[i]=='knife' or labels[i]=='apple' or labels[i]=='chair' or  labels[i]=='remote' or labels[i]=='dining table' or labels[i]=='laptop' or labels[i]=='mouse' or labels[i]=='cell phone' or labels[i]=='toothbrush':

                        nobj=nobj+1
                        left =int(xmin[i])+15
                        top = int(ymin[i])+10
                        right =int(xmax[i])-10
                        bottom = int(ymax[i])-10
                        
                        width = right - left
                        height = bottom - top
                        if cngp:
                           yp=bottom
                           cngp=False
                        else:
                           yp=top
                           cngp=True
                        
                        bbox = (int(left), int(top), int(width), int(height))

                        p1 = (int(bbox[0]), int(bbox[1]))
                        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                        p3=(int(xmax[i]),int(ymax[i]))
                        cv2.rectangle(image2, p1, p3, (255, 0, 0), 2, 1)

                        # x,y,z of bounding box
                        #obj_points = verts[left:right,top:bottom].reshape(-1, 3)
                        obj_points = verts[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2])].reshape(-1, 3)


                        zs = obj_points[:,2]

                        z = np.median(zs)

                        ys = obj_points[:,1]
                        ys = np.delete(ys, np.where((zs < z - 1) | (zs > z + 1))) # take only y for close z to prevent including background
                        my = np.amin(ys, initial=1)
                        My = np.amax(ys, initial=-1)
                        Mym = np.median(ys)
                        
                        xs = obj_points[:,0]
                        xs = np.delete(xs, np.where((zs < z - 1) | (zs > z + 1))) # take only x for close z to 
                        mx = np.amin(xs, initial=1)
                        Mx = np.amax(xs, initial=-1)
                        Mxm = np.median(xs)
                       
                        height = (My - my)   # add next to rectangle print of height using cv library
                        weight_=(Mx - mx)
                        lenth_=z
                        try:
                            height = round(float("{:.2f}".format(height)))
                            weight_ =round( float("{:.2f}".format(weight_)))
                            lenth_ = round(float("{:.2f}".format(lenth_)))
                        except:
                            pass
                        #print("[INFO] object height is: ", height, "[m]")
                        #height_txt = str(height)+"H , "+str(weight_)+"W , "+str(lenth_)+"L [cm]" 
                       
                        # z=z*100
                        # mx=mx*100
                        # Mx=Mx*100
                        # my=my*100
                        # My=My*100
                        
                        # z=z
                        # mx=mx
                        # Mx=Mx
                        # my=my
                        # My=My

                        z = float("{:.2f}".format(z))
                        mx = float("{:.2f}".format(mx))
                        Mx = float("{:.2f}".format(Mx))
                        Mxm = float("{:.2f}".format(Mxm))
                                   
                        my = float("{:.2f}".format(my))
                        My = float("{:.2f}".format(My))
                        Mym = float("{:.2f}".format(Mym))

                        #print("[INFO] object height is: ", height, "[m]")
                        height_txt = str(nobj)+ " = "+  str(Mxm)+" Mxm , "+str(mx)+" mx , "+str(Mx)+" Mx , "+str(Mym)+" Mym , "+ str(my)+" my , "+str(My)+" My , "+str(z)+"L [m]" 
                       
                        # Write some Text
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        #bottomLeftCornerOfText = (p1[0], yp+20)
                        bottomLeftCornerOfText = (p1[0], yp+20)
                        bottomLeftCornerOfText1 = (20,nobj*20)
                        fontScale = 0.6
                        fontColor = (0, 0, 255)
                        lineType =2
                        height_txt =str(nobj)+"  "+height_txt
                        obj_l.append(height_txt)
                        cv2.putText(image2, height_txt,
                                    bottomLeftCornerOfText1,
                                    font,
                                    fontScale,
                                    fontColor,
                                    lineType)
                        
                        cv2.putText(image2, str(nobj),
                                    bottomLeftCornerOfText,
                                    font,
                                    fontScale,
                                    fontColor,
                                    lineType)
            
            return image2,obj_l
    def obstacle_box(self,boxs,verts):
                   obs=" "
                   for box in boxs:
                        obspos = verts[box[1]:box[3],box[0]:box[2]].reshape(-1, 3)
                        zs = obspos[:,2]
                        z = np.median(zs)
                
                        zs = np.delete(zs, np.where((zs < z - 1) | (zs > z + 1))) 
                        zm = np.amin(zs, initial=1)

                        z = float("{:.2f}".format(z))
                        zm = float("{:.2f}".format(zm))

                        obs =obs+ " obs : "+ str(z)+"L [m] " +str(zm)+" minL[m]" 
                    
                   return obs
                        
    def get_only_xyz_len(self,image,verts,boxs):
            image2 = copy.deepcopy(image)
            imgsbox = self.model(image).pandas().xyxy[0]
            Mxm=0
            Mym=0
            z=0
            height_=0 
            weight_=0
            labels = imgsbox['name']
            xmin =  imgsbox['xmin']
            ymin =  imgsbox['ymin']
            xmax =  imgsbox['xmax']
            ymax =  imgsbox['ymax']
            conf = imgsbox["confidence"]
            cngp=False
            nobj=0
            obj_l=[]
            #obstacle=[340,470,350,564] #[10,470,284,564]
            
            obs=self.obstacle_box(boxs,verts)
            
            for i in range(len(labels)):
                if round(conf[i] ,3)>0.50:
                    if labels[i]== 'bottle':
                    # labels[i]=='__background__' or
                    # if labels[i]=='__background__' or labels[i]== 'person' or labels[i]=='handbag' or labels[i]=='tie'  or labels[i]=='suitcase' or labels[i]=='sports ball' or labels[i]=='baseball bat' or labels[i]=='bottle' or labels[i]=='cup' or labels[i]=='knife' or labels[i]=='apple' or labels[i]=='chair' or  labels[i]=='remote' or labels[i]=='dining table' or labels[i]=='laptop' or labels[i]=='mouse' or labels[i]=='cell phone' or labels[i]=='toothbrush':

                        nobj=nobj+1
                        left =int(xmin[i])+15
                        top = int(ymin[i])+10
                        right =int(xmax[i])-10
                        bottom = int(ymax[i])-10
                        width = right - left
                        height = bottom - top
                        
                        bbox = (int(left), int(top), int(width), int(height))

                        obj_points = verts[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2])].reshape(-1, 3)


                        zs = obj_points[:,2]

                        z = np.median(zs)

                        ys = obj_points[:,1]*-1
                        ys = np.delete(ys, np.where((zs < z - 1) | (zs > z + 1))) 
                        
                        my = np.amin(ys, initial=1)
                        My = np.amax(ys, initial=-1)
                        Mym = np.median(ys)
                        
                        xs = obj_points[:,0]*-1
                        xs = np.delete(xs, np.where((zs < z - 1) | (zs > z + 1))) 
                        
                        mx = np.amin(xs, initial=1)
                        Mx = np.amax(xs, initial=-1)
                        Mxm = np.median(xs)
                        # try:
                        #     height = round(float("{:.2f}".format(height)))
                        #     weight_ =round( float("{:.2f}".format(weight_)))
                        #     lenth_ = round(float("{:.2f}".format(lenth_)))
                        # except:
                        #     pass

                        z = float("{:.2f}".format(z))
                        mx = float("{:.2f}".format(mx))
                        Mx = float("{:.2f}".format(Mx))
                        Mxm = float("{:.2f}".format(Mxm))
                                   
                        my = float("{:.2f}".format(my))
                        My = float("{:.2f}".format(My))
                        Mym = float("{:.2f}".format(Mym))
                        try:
                            height_ = (My - my)   
                            weight_=(Mx - mx)
                        except:
                            pass
                   
                        height_txt = str(nobj)+ " = "+  str(Mxm)+" Mxm , "+str(mx)+" mx , "+str(Mx)+" Mx , "+str(Mym)+" Mym , "+ str(my)+" my , "+str(My)+" My , "+str(z)+"L [m]" 
                       
 
                        height_txt =str(nobj)+"  "+height_txt
                        obj_l.append(height_txt)
     
 

             
            return  obj_l,[Mxm,Mym,z],[height_,weight_],obs
        
