import torch
import os
import cv2
import numpy as np
import copy

class track_obj:
    def __init__(self):
          #self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='./libs/yolov5s.pt', force_reload=True).autoshape()
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s') 
        self.objects=[]
    
    def getcropperpos(self,area,verts):
                 xyz=[0,0,0]
                 try:
                        top=area[0][1]
                        bottom=area[1][1]
                        left=area[0][0]
                        right=area[1][0]
                        
                        obj_points = verts[ top:bottom , left:right ].reshape(-1, 3)
                        xmin = verts[ top:bottom , left:left+10 ].reshape(-1, 3)
                        xmax = verts[ top:bottom , right-10:right ].reshape(-1, 3)
                        ymin=verts[ top:top+10 , left:right ].reshape(-1, 3)
                        ymax=verts[ bottom-10:bottom , left:right ].reshape(-1, 3)
                        
                        z = obj_points[:,2]
                        zmid = np.around(np.median(z),3)

                        x= obj_points[:,0]
                        xs = np.delete(x, np.where( (z < zmid - 1) | (z > zmid + 1) ))   
                        xs = xs[xs!= 0]
                        xmid =np.around( np.median(xs),3)

                        xmin1 = xmin[:,0]
                        zz = xmin[:,2]
                        xs = np.delete(xmin1, np.where( (zz < zmid - 1) | (zz > zmid + 1) ))   
                        xs = xs[xs!= 0]
                        xm = np.around( np.amax(xs),3)

                        xmin1 = xmax[:,0] 
                        xs = np.delete(xmin1, np.where( (zz < zmid - 1) | (zz > zmid + 1) ))   
                        xs = xs[xs!= 0]
                        XM = np.around( np.amin(xs),3)

                        # xm = np.around(np.amin(xs),3)
                        # XM = np.around(np.amax(xs),3)

                        y = obj_points[:,1]
                        ys = np.delete(y, np.where((z < zmid - 1) | (z > zmid + 1)))
                        ys = ys[ys!= 0]
                        ymid = np.around(np.median(ys),3)


                        ymin1 = ymin[:,1]
                        zz = ymin[:,2]
                        ys = np.delete(ymin1, np.where( (zz < zmid - 1) | (zz > zmid + 1) ))   
                        ys = ys[ys!= 0]
                        ym = np.around( np.amax(ys),3)

                        ymax1 = ymax[:,0] 
                        ys = np.delete(ymax1, np.where( (zz < zmid - 1) | (zz > zmid + 1) ))   
                        ys = ys[ys!= 0]
                        YM = np.around( np.amin(ys),3)

                        # ym = np.around(np.amin(ys),3)
                        # YM = np.around(np.amax(ys),3)

                        z = z[z!=0]
                        zm =np.around( np.amin(z),3)

                        xt=[xm,xmid,XM]
                        yt=[ym,ymid,YM]
                        zt=[zm,zmid]
                        xyz=[xt,yt,zt]
                         
                 except:
                    xyz=[1,1,1]
                     
                 return  xyz             
                
    def calculat(self,image,verts,depth_image):
            image2 = copy.deepcopy(image)
            imgsbox = self.model(image).pandas().xyxy[0]
             
            labels = imgsbox['name']
            xmin =  imgsbox['xmin']
            ymin =  imgsbox['ymin']
            xmax =  imgsbox['xmax']
            ymax =  imgsbox['ymax']
            conf = imgsbox["confidence"]
          
            obj_l=[]
            h, w, c = image2.shape
            image2 = cv2.line(image2, (0, int(h/2)), (w, int(h/2)), (0, 0, 250), 3)
            image2 = cv2.line(image2, (int(w/2) , 0), (int(w/2),h), (0, 0, 250), 3)
                
#             depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
#             depth_colormap = cv2.line(depth_colormap, (0, int(h/2)), (w, int(h/2)), (0, 0, 250), 3)
#             depth_colormap = cv2.line(depth_colormap, (int(w/2) , 0), (int(w/2),h), (0, 0, 250), 3)   
        
#             depth_colormap_dim = depth_colormap.shape
#             color_colormap_dim = image2.shape
 
            xyz=[0,0,0]
            self.objects=[]
            for i in range(len(labels)):
                if round(conf[i] ,3)>0.50:
                    if labels[i]== 'bottle':
                        
                        left =int(xmin[i]) #+15
                        top = int(ymin[i]) #+10
                        right =int(xmax[i]) #-10
                        bottom = int(ymax[i]) #-10
                        
                        width = right - left
                        height = bottom - top

                        bbox = (int(left), int(top), int(width), int(height))

                        p1 = (int(bbox[0]), int(bbox[1]))
                        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                        p3=(int(xmax[i]),int(ymax[i]))
                        
                        cv2.rectangle(image2, p1, p3, (255, 0, 0), 2, 1)
                        #cv2.rectangle(depth_colormap, p1, p3, (255, 0, 0), 2, 1)
                        try:
                                obj_points = verts[ top:bottom , left:right ].reshape(-1, 3)
                                xmin = verts[ top:bottom , left:left+10 ].reshape(-1, 3)
                                xmax = verts[ top:bottom , right-10:right ].reshape(-1, 3)
                                ymin=verts[ top:top+10 , left:right ].reshape(-1, 3)
                                ymax=verts[ bottom-10:bottom , left:right ].reshape(-1, 3)
                                #depth_image=depth_image[top:bottom , left:right ]
                                #obj_points = verts[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2])].reshape(-1, 3)

                                z = obj_points[:,2]
                                zmid = np.around(np.median(z),3)
                                
                                x= obj_points[:,0]
                                xs = np.delete(x, np.where( (z < zmid - 1) | (z > zmid + 1) ))   
                                xs = xs[xs!= 0]
                                xmid =np.around( np.median(xs),3)
                                
                                xmin1 = xmin[:,0]
                                zz = xmin[:,2]
                                xs = np.delete(xmin1, np.where( (zz < zmid - 1) | (zz > zmid + 1) ))   
                                xs = xs[xs!= 0]
                                xm = np.around( np.amax(xs),3)
                                
                                xmin1 = xmax[:,0] 
                                xs = np.delete(xmin1, np.where( (zz < zmid - 1) | (zz > zmid + 1) ))   
                                xs = xs[xs!= 0]
                                XM = np.around( np.amin(xs),3)
                                
                                # xm = np.around(np.amin(xs),3)
                                # XM = np.around(np.amax(xs),3)
                               
                                y = obj_points[:,1]
                                ys = np.delete(y, np.where((z < zmid - 1) | (z > zmid + 1)))
                                ys = ys[ys!= 0]
                                ymid = np.around(np.median(ys),3)
                                
                                
                                ymin1 = ymin[:,1]
                                zz = ymin[:,2]
                                ys = np.delete(ymin1, np.where( (zz < zmid - 1) | (zz > zmid + 1) ))   
                                ys = ys[ys!= 0]
                                ym = np.around( np.amax(ys),3)
                                
                                ymax1 = ymax[:,0] 
                                ys = np.delete(ymax1, np.where( (zz < zmid - 1) | (zz > zmid + 1) ))   
                                ys = ys[ys!= 0]
                                YM = np.around( np.amin(ys),3)
                                
                                # ym = np.around(np.amin(ys),3)
                                # YM = np.around(np.amax(ys),3)
                                
                                z = z[z!=0]
                                zm =np.around( np.amin(z),3)

                                xt=[xm,xmid,XM]
                                yt=[ym,ymid,YM]
                                zt=[zm,zmid]
                                xyz=[xt,yt,zt]
                                self.objects.append([xyz,True])
                        except:
                          xyz=[1,1,1]
                          self.objects.append([xyz,False])
                        # cv2.putText(
                        #             image2, 
                        #             str(nobj),
                        #             bottomLeftCornerOfText,
                        #             font,
                        #             fontScale,
                        #             fontColor,
                        #             lineType)
                        
            
            
            # if depth_colormap_dim != color_colormap_dim:
            #     resized_color_image = cv2.resize(image2, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            #     image2 = np.hstack((resized_color_image, depth_colormap))
            # else:
            #     image2 = np.hstack((image2, depth_colormap))  
                
            return image2 ,self.objects
        
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
                    if labels[i]== 'bottle':
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

                        obj_points = verts[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2])].reshape(-1, 3)
                        
                        zs = obj_points[:,2]
                        z = np.median(zs)
                        
                        xs = obj_points[:,0]
                        xs = np.delete(xs, np.where((zs < z - 1) | (zs > z + 1)))   
                        
                        mx = np.amin(xs, initial=1)
                        Mx = np.amax(xs, initial=-1)
                        Mxm = np.median(xs)
                        
                        ys = obj_points[:,1]*-1
                        ys = np.delete(ys, np.where((zs < z - 1) | (zs > z + 1)))
                        
                        my = np.amin(ys, initial=1)
                        My = np.amax(ys, initial=-1)
                        Mym = np.median(ys)
                        
                       

                        
                        
                        
                        
                        # new 
                        xs = obj_points[:,0]*-1
                        xs = np.delete(xs, np.where((zs < z - 1) | (zs > z + 1))) 
                        
                        ys = obj_points[:,1]*-1
                        ys = np.delete(ys, np.where((zs < z - 1) | (zs > z + 1))) 
                        
                        my = np.amin(ys, initial=1)
                        My = np.amax(ys, initial=-1)
                        Mym = np.median(ys)
  
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

                        z = float("{:.2f}".format(z))
                        mx = float("{:.2f}".format(mx))
                        Mx = float("{:.2f}".format(Mx))
                        Mxm = float("{:.2f}".format(Mxm))
                                   
                        my = float("{:.2f}".format(my))
                        My = float("{:.2f}".format(My))
                        Mym = float("{:.2f}".format(Mym))

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
        
