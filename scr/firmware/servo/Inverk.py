import copy
import math
import threading

import numpy as np
import tinyik

"""
1. Find the object postion 
2. Confirmnation of the side like left , right , top ,bottom and iner side of hands and outer side of hands 
3. Objects reset or robot go to the object to enter into the working area.
4. Posable gripping side , like left, roght , top , bottom 
5. Invers kinematic 
6  gripp the object 
"""

class Roba_Robotf:
      
      def __init__(self):
            # import platform
            # print(platform.python_version())
            sf=100
            l1=5.8/sf
            l2=10.3/sf
            
            l3=9/sf
            l4=5.7/sf
            
            self.end_p = 7.0/sf
            # h1=[0,0.14252,0] 
            # h2=[0,0.11498,0] 
            # h3=[0,0,0.06465]  
            #Right_hand_join_rotation_limet
            self.RHJRL = [[0,0],[-180,90],[-200,0],[-180,180],[-95,0],[-120,120],[-80,80]]
            self.LHJRL = [[0,0],[-180,90],[200,-20],[180,-180],[-95,0],[120,-120],[-80,0]]
            
            self.link1 =l1+l2 # 0.161 
            self.link2 =l3+l4 # 0.147
            
            self.total_l = self.link1+self.link2
            self.total_len = self.link1 + self.link2 + self.end_p
            alljoin  =[l1,l2,l3,l4,self.end_p]
            
            self.llj1 = [0.166 , 0 , 0.016]
            self.lj1 = [-0.166 , 0 , 0.016]
            self.lj2 = [-0.166- l1  ,0  , 0.016]
            self.lj3 = [-0.166 - (l1+l2), 0  , 0.016]
            
            self.lj4 = [-0.166 - (l1+l2+l3),0, 0.016] 
            self.lj5 = [-0.166 - (l1+l2+l3+l4),0 , 0.016]
            
            self.lj6 = [-0.166 - (l1+l2+l3+l4+self.end_p) ,0, 0.03] #0.028
            
            self.h1=[0,0.14252,0] 
            self.h2=[0,0.11498,0.06465] 
       
      def came_get_pos_obj(self):
            pass
      def obj_pos(self,obj):
          updo = 0
          lefriht = 0
           
          if obj[0] > self.lj1[0]:
             lefriht = 1 
          elif obj[0] < self.lj1[0]:
               lefriht = 2
           
          if obj[1] > 0:
             updo = 1
             
          elif obj[1] < 0:
               updo = 2
          return lefriht , updo 
      
      def get_xyz_len1(self,n,o):
      
            npo =[]
           
            for i in range(0,3):
               
                if n[i]<=0 and o[i]<=0:
                    
                     if n[i]>o[i]:
                        npo.append((o[i] - n[i]) * -1 )
                     else:
                         npo.append( (n[i] - o[i]) * -1 )
                         
                elif n[i]>=0 and o[i]<=0:
                      npo.append( n[i] + (o[i] * -1))
                elif n[i]<=0 and o[i]>=0:
                     npo.append( ((n[i]* -1) + o[i]) * -1 )
                elif n[i]>=0 and o[i]>=0:
                
                        if n[i]>o[i]:
                            
                           npo.append( n[i]  - o[i] )
                        else:
                            
                           npo.append(o[i] - n[i] )
            
            return npo
      
      def get_obj_range(self,xyz):
            
            a = math.atan(xyz[0]/xyz[2])
            h = xyz[2]/math.cos(a)
            a1 = math.atan(xyz[1]/h)
            h1 = h/math.cos(a1)
            a = np.rad2deg(a)
            a1 = np.rad2deg(a1)

            return [a,h,a1,h1]
     
      def working_area_cal(self,Tobj,Spos):
          
          xyzpos  = self.get_xyz_len1(Tobj,Spos)  
          xyzlen  = self.get_obj_range(xyzpos)
          return xyzlen 
 
      def get_wrking_area(self,obj):
      
          lefthandorg = copy.deepcopy(self.lj1) 
          #self.total_len
          rans = [0,0,0]
          lenth=0
          if  (obj[1]<0) and (obj[1] < - (self.link1+self.link2)):

                 rans[1] = obj[1] + self.link1+self.link2
                 
          elif (obj[1]>0)   and (obj[1] > (self.link1+self.link2)): 
          
                rans[1] = obj[1] - self.link1+self.link2
                
          if ( obj[2] < 0.22 and ( obj[0] > - (0.22+0.166) and   obj[0] < (0.22+0.166)  )):
                
               rans[2] =obj[2] -0.22
          else:
            lin1pos9 = self.working_area_cal(obj,lefthandorg)
            #print(lin1pos9 , " dist 2 3D obj")
            lenth = lin1pos9[3]
            if lin1pos9[3]>0.35:
               
               while lin1pos9[3]>0.35:
               
                     if  lin1pos9[0]>45:
                         obj[0] = obj[0]+0.001
                         rans[0] = rans[0]+0.001
                         lin1pos9 = self.working_area_cal(obj,lefthandorg)
                     else:
                         obj[2] = obj[2]-0.001
                         rans[2] = rans[2]+0.001
                         lin1pos9 = self.working_area_cal(obj,lefthandorg)
               
          return rans ,lenth  
      
      def yxang(self,robaLhandL1, join1ang2,obj,newcon4): 
                   

                    anglen = self.working_area_cal(obj,newcon4)
                    
                    
                    #robaLhandL7.ee = self.lj6
                    #np.deg2rad(90-anglen[2])
                    join1ang2 = [join1ang2[0],join1ang2[1],0,0,0,0 ]

                    robaLhandL7 = tinyik.Actuator([ self.lj1,"x","z",[-self.link1 , 0 ,0],"x","y",[-self.link2,0,0]  ,"x","y",[-self.end_p,0,0] ,[0,0,self.total_len-self.link2]])
                    robaLhandL7.angles = join1ang2
                    newcon2 = copy.deepcopy(robaLhandL7.ee)

                    robaLhandL1.angles = join1ang2
                    newcon7 = copy.deepcopy(robaLhandL1.ee)
                    newcon7= copy.deepcopy(newcon7)
                    i=0
                    join1ya=1
                    join1xa=1
                    yac=True
                    xac=True
                    ya=0
                    xa=0
                    xc=False
                    yc=False
                    zc=False
                    h=0
                    yang=0
                    count =0
                    
                    for l in range(i,180):
                        i=l
                        if newcon2[1]>obj[1]:
                            join1ang2[2] = np.deg2rad(l)
                            robaLhandL7.angles = join1ang2
                            newcon2 =  robaLhandL7.ee
                            if round( (newcon2[1] - obj[1]),3 ) <= 0.0:
                                break
                        else:
                            join1ang2[2] = np.deg2rad(-l)
                            robaLhandL7.angles = join1ang2
                            newcon2 =  robaLhandL7.ee
                            if round( (obj[1] -newcon2[1] ),3 ) <= 0.0:
                                break
                    yang =  join1ang2[2]
                    #and round( ( obj[2] - newcon2[2]),3 ) <= 0.01
                    #and round( ( obj[2] - newcon2[2]) ,3 ) > 0.01
                     
                    
                    while True:
                        count=count+1
                        if count==1000:
                             break
                        if obj[0]<0 and newcon2[0] <0:
                            if obj[0]>newcon2[0] :
                                if round( (obj[0] - newcon2[0] ),3 ) > 0.01 :
                                    join1ang2[3] = np.deg2rad(np.rad2deg(join1ang2[3]) +1)
                                    robaLhandL1.angles = join1ang2
                                    newcon2 =  robaLhandL1.ee
                                    ya=ya+1
                                    if round( (obj[0] - newcon2[0] ),3 ) <= 0.01 and round( (obj[0] - newcon2[0] ),3 ) >=0:
                                     break
                                else:
                                    xc=False
                                    for k in range(180):

                                            if obj[1] > newcon2[1] :
                                                if round( (obj[1] - newcon2[1] ),3 ) > 0.01 :
                                                        join1ang2[2] = np.deg2rad(np.rad2deg(join1ang2[2]) -1)
                                                        robaLhandL1.angles = join1ang2
                                                        newcon2 =  robaLhandL1.ee     
                                                if round( (obj[1] - newcon2[1] ),3 ) <= 0.01 :
                                                            xc=True
                                                            break
                                            else:
                                                if round( (newcon2[1] -obj[1]),3 ) > 0.01:
                                                        join1ang2[2] = np.deg2rad(np.rad2deg(join1ang2[2]) +1)
                                                        robaLhandL1.angles = join1ang2
                                                        newcon2 =  robaLhandL1.ee
                                                        
                                                if round(  (newcon2[1] -obj[1]),3 ) <= 0.01  :
                                                            xc=True
                                                            break
                                        
                            else:
                                xa=xa+1
                                if round( (newcon2[0] - obj[0]),3 ) > 0.01 :
                                    join1ang2[3] = np.deg2rad(np.rad2deg(join1ang2[3]) -1)
                                    robaLhandL1.angles = join1ang2
                                    newcon2 =  robaLhandL1.ee
                                    if round( (newcon2[0] -obj[0] ),3 ) <= 0.01 and round( (newcon2[0] -obj[0] ),3 ) >=0:
                                        break
 
                                else:
                                    xc=False
                                    for k in range(180):
                                   
 
                                            if obj[1] > newcon2[1] :
                                                if round( (obj[1] - newcon2[1] ),3 ) > 0.01 :
                                                        join1ang2[2] = np.deg2rad(np.rad2deg(join1ang2[2]) -1)
                                                        robaLhandL1.angles = join1ang2
                                                        newcon2 =  robaLhandL1.ee
                                                         
                                                if round( (obj[1] - newcon2[1] ),3 ) <= 0.01  :
                                                            xc=True
                                                            break
                                            else:
                                                if round( (newcon2[1] -obj[1]),3 ) > 0.01:
                                                        join1ang2[2] = np.deg2rad(np.rad2deg(join1ang2[2]) +1)
                                                        robaLhandL1.angles = join1ang2
                                                        newcon2 =  robaLhandL1.ee
                                                         
                                                if round(  (newcon2[1] -obj[1]),3 ) <= 0.01  :
                                                            xc=True
                                                            break
                            
                            # if  xc and np.rad2deg(join1ang2[3])>=95 or xc and np.rad2deg(join1ang2[3])<=0:
                            #     break
                    print(xa,ya,join1xa,join1ya,count, "  counting .........")   
                    join1ang2[2]=yang 
                    robaLhandL1.angles = join1ang2
                    newcon2 =  robaLhandL1.ee
                    for k in range(180):

                                if obj[1] > newcon2[1] :
                                    if round( (obj[1] - newcon2[1] ),3 ) > 0.01 :
                                            join1ang2[2] = np.deg2rad(np.rad2deg(join1ang2[2]) -1)
                                            robaLhandL1.angles = join1ang2
                                            newcon2 =  robaLhandL1.ee
                                                
                                    if round( (obj[1] - newcon2[1] ),3 ) <= 0.01  :
                                                break
                                else:
                                    if round( (newcon2[1] -obj[1]),3 ) > 0.01:
                                            join1ang2[2] = np.deg2rad(np.rad2deg(join1ang2[2]) +1)
                                            robaLhandL1.angles = join1ang2
                                            newcon2 =  robaLhandL1.ee
                                                
                                    if round(  (newcon2[1] -obj[1]),3 ) <= 0.01  :
                                                break
                    robaLhandL7 = tinyik.Actuator([ self.lj1,"x","z",[-self.link1 , 0 ,0],"x","y",[-self.link2,0,0]  ,"x","y",[-self.end_p,0,0] ,[0,0,self.link2 ]])
                    robaLhandL7.angles = join1ang2
                    newcon7 =  robaLhandL1.ee

                    for l in range(i,180):
                        i=l
                        if newcon7[1] <obj[1]:
                            join1ang2[4] = np.deg2rad(l)
                            robaLhandL7.angles = join1ang2
                            newcon7 =  robaLhandL7.ee
                            if round( (newcon7[1] - obj[1]),3 ) <= 0.0:
                                break
                        else:
                            join1ang2[4] = np.deg2rad(-l)
                            robaLhandL7.angles = join1ang2
                            newcon7 =  robaLhandL7.ee
                            if round( ( obj[1] -newcon7[1] ),3 ) <= 0.0:
                                break

                     

                    print(i," iter")
                    join1ang2 = np.rad2deg(join1ang2)
                    if count==1000:
                        join1ang2=[0,0,0,0,0,0]
                    return newcon2 ,join1ang2 

      
      def invrkr7(self,obj):
          self.lj6

          robaLhandL1 = tinyik.Actuator([ obj,"y","x",[ 0 , 0 , - (self.link2+self.end_p)]])
          robaLhandL1.ee = self.lj6
          #ang1 = np.rad2deg(robaLhandL1.angles)
          newcon2 = robaLhandL1.ee
          newcon1=newcon2
          
          robaLhandL2 = tinyik.Actuator([ self.lj1,"x","z",[-self.link1 , 0 ,0]])
          robaLhandL2.ee = newcon1
          newcon1=robaLhandL2.ee
          ang2 =  robaLhandL2.angles
          ang1 = np.rad2deg(ang2)
         
          robaLhandL3 = tinyik.Actuator([ newcon1 ,"x","z","x","y",[-self.link2,0,0]  ,"x","y",[-self.end_p,0,0] ])
 
          newcon1,join1ang23 = self.yxang(robaLhandL3,ang2,obj,newcon1)
 
          LH_joinA= [ang1[0],ang1[1]-90,join1ang23[2],-join1ang23[3],0,0 ]
          
          #LH_joinA= [ang1[0],ang1[1]-90,0,0,0,0 ]
          dire=[0,0,0]
          return  newcon1 , LH_joinA ,dire
 

      # [-0.325506, 0.84233, 0.22]
      def get_global_pos(self,deg):
            Global_pos_obj = tinyik.Actuator([self.lj1,'x','z',[0,-self.link1,0],'y','x',[0,-self.link2,0],'y','x',[0,-self.end_p,0]])
            
            Global_pos_obj.angles=np.deg2rad([deg[0],deg[1],deg[2],deg[3],deg[4] ,deg[5] ])
        
            return Global_pos_obj.ee
            
      def robot_Invk(self,obj):
          
          newcon=0
          join1ang=0
          obj[1] = obj[1] #- 0.97
          newcon =obj
          #rans=[0,0,0]
          rans,lenth = self.get_wrking_area(obj)
          ext=False
          if ( rans[0]>=-0.01 and rans[0]<=0.01)  and ( rans[1]>=-0.01 and rans[1]<=0.01) and ( rans[2]>=-0.01 and rans[2]<=0.01):
                 if obj[0]<=0:
                   newcon,join1ang,rans= self.invrkr7(obj)
                   if ( rans[0]>=-0.02 and rans[0]<=0.02)  and ( rans[1]>=-0.02 and rans[1]<=0.02) and ( rans[2]>=-0.02 and rans[2]<=0.02):
                        ext=True
                   else:    
                      print(rans," please position the obj")  
          else: 
            print(rans," please position the obj")  
            
          return newcon,join1ang,ext

    
      def rePos_r(self,pos):
          Global_pos_obj = tinyik.Actuator([pos,'x','y', [0,0,-(self.link2+self.end_p)] ])
          # self.llj1
          Global_pos_obj.ee =self.llj1
          ang = np.rad2deg(Global_pos_obj.angles)
          spos = Global_pos_obj.ee
          eror_pos = self.working_area_cal(self.llj1,spos)
          gspos=0
          if spos[1]>0:
                gspos=1000
                i=1
                while eror_pos[3]<self.link1:
                        ang[0]=ang[0]+i
                        i=i+1
                        Global_pos_obj.angles=np.deg2rad(ang)
                        spos = Global_pos_obj.ee
                        eror_pos = self.working_area_cal(self.llj1,spos)
                        if gspos<eror_pos[3]:
                            i=i-3
                            break
                        gspos=eror_pos[3]

          elif spos[1]<0:
                gspos=-1000
                i=-1
                while eror_pos[3]<self.link1:
                        ang[0]=ang[0]+i
                        i=i-1
                        Global_pos_obj.angles=np.deg2rad(ang)
                        spos = Global_pos_obj.ee
                        eror_pos = self.working_area_cal(self.llj1,spos)
                        if gspos>eror_pos[3]:
                            i=i+3
                            break
                        gspos=eror_pos[3]
                        
          i=1
          while eror_pos[3]<self.link1:
                ang[1]=ang[1]-i
                i=i+1
                Global_pos_obj.angles=np.deg2rad(ang)
                spos = Global_pos_obj.ee
                eror_pos = self.working_area_cal(self.llj1,spos)
            
          return spos

      def get_joint_ang_Right_hand(self,pos):
            pos1  = copy.deepcopy(pos)
            lnpos =self.rePos_r(pos)

            Global_pos_obj = tinyik.Actuator([self.llj1,'x','z',[0,-self.link1,0]])
            Global_pos_obj.ee = lnpos
            gang1 = Global_pos_obj.angles
            gang =np.rad2deg(Global_pos_obj.angles)
            lnpos = Global_pos_obj.ee

            if gang[1]>200:
               gang[1]=200
            elif gang[1]<-20:
                 gang[1]=-20
            Global_pos_obj.angles=np.deg2rad(gang)
            lnpos = Global_pos_obj.ee
            gang1 = Global_pos_obj.angles
            gang =np.rad2deg(Global_pos_obj.angles)

            Global_pos_obj1 = tinyik.Actuator([self.llj1,'x','z',[0,-(self.link1+self.link2+self.end_p),0]])
            Global_pos_obj1.angles = Global_pos_obj.angles
            lnpos1 = Global_pos_obj1.ee
            
            Global_pos_obj2 = tinyik.Actuator([lnpos,'y','x',[lnpos1[0],lnpos1[1],lnpos1[2]]])
            Global_pos_obj2.ee = pos1
            gangs2 = Global_pos_obj2.angles
            gang2 =np.rad2deg(Global_pos_obj2.angles)
            lnpos2 = Global_pos_obj2.ee

            Global_pos_obj3 = tinyik.Actuator([lnpos,'x','z','y','x',[0,-(self.link2+self.end_p),0]])
            Global_pos_obj3.angles = [gang1[0],gang1[1],gangs2[0],0]
            lnpos3=Global_pos_obj3.ee
            #
            eror_pos = self.working_area_cal(pos1,lnpos3)
            i=-1
            eror_pos2=10
             
            for k in range(96):     
                i=i-1
                if eror_pos2>eror_pos[3]:
                    eror_pos2=eror_pos[3]
                else:
                    break
                Global_pos_obj3.angles = [gang1[0],gang1[1],gangs2[0],np.deg2rad(i)]
                lnpos3=Global_pos_obj3.ee
                eror_pos = self.working_area_cal(pos1,lnpos3)
            eror_pos2=1000
            gangs3 = Global_pos_obj3.angles
            if eror_pos[3]>0.005:
                if pos1[1]>lnpos3[1] :
                    i=0
                    for k in range(90):     
                            i=i+1
                            if eror_pos2>eror_pos[3]:
                                eror_pos2=eror_pos[3]
                            else:
                                break
                            Global_pos_obj3.angles = [gang1[0],gang1[1],gangs2[0]+np.deg2rad(i),gangs3[3]]
                            lnpos3=Global_pos_obj3.ee
                            eror_pos = self.working_area_cal(pos1,lnpos3)
                elif pos1[1]<lnpos3[1] :
                    i=0
                    for k in range(90):     
                            i=i-1
                            if eror_pos2>eror_pos[3]:
                                eror_pos2=eror_pos[3]
                            else:
                                break
                            Global_pos_obj3.angles = [gang1[0],gang1[1],gangs2[0]+np.deg2rad(i),gangs3[3]]
                            lnpos3=Global_pos_obj3.ee
                            eror_pos = self.working_area_cal(pos1,lnpos3)
            
            
            gang3 =np.rad2deg(Global_pos_obj3.angles)
            
            eror_pos = self.working_area_cal(pos1,lnpos3)

            rang=True 
            if eror_pos[3]>0.02:
               rang=False
               print(" out of range go to Object ",eror_pos[3])
            if pos1[2]<0.22:
                rang=False
                print(" very close minmum range 0.22 but get",round(pos1[2],2) ," go back the Object", 0.22 - pos1[2])
                
            return [gang[0],gang[1],gang3[2],gang3[3]],lnpos3,rang
            
         
      def rePos_l(self,pos):
          Global_pos_obj = tinyik.Actuator([pos,'x','y', [0,0,-(self.link2+self.end_p)] ])
          # self.llj1
          Global_pos_obj.ee =self.lj1
          ang = np.rad2deg(Global_pos_obj.angles)
          spos = Global_pos_obj.ee
          eror_pos = self.working_area_cal(self.lj1,spos)
          
          gspos=0
          if spos[1]>0:
                gspos=1000
                i=1
                while eror_pos[3]<self.link1:
                        ang[0]=ang[0]+i
                        i=i+1
                        Global_pos_obj.angles=np.deg2rad(ang)
                        spos = Global_pos_obj.ee
                        eror_pos = self.working_area_cal(self.lj1,spos)
                        if gspos<eror_pos[3]:
                            i=i-3
                            break
                        gspos=eror_pos[3]

          elif spos[1]<0:
                gspos=-1000
                i=-1
                while eror_pos[3]<self.link1:
                        ang[0]=ang[0]+i
                        i=i-1
                        Global_pos_obj.angles=np.deg2rad(ang)
                        spos = Global_pos_obj.ee
                        eror_pos = self.working_area_cal(self.lj1,spos)
                        if gspos>eror_pos[3]:
                            i=i+3
                            break
                        gspos=eror_pos[3]
                        
        
        
          i=1
          while eror_pos[3]<self.link1:
                ang[1]=ang[1]+i
                i=i+1
                Global_pos_obj.angles=np.deg2rad(ang)
                spos = Global_pos_obj.ee
                eror_pos = self.working_area_cal(self.lj1,spos)
            
          return spos

      def get_joint_ang_left_hand(self,pos):
            pos1  = copy.deepcopy(pos)
            lnpos =self.rePos_l(pos)

            Global_pos_obj = tinyik.Actuator([self.lj1,'x','z',[0,-self.link1,0]])
            Global_pos_obj.ee = lnpos
            gang1 = Global_pos_obj.angles
            gang =np.rad2deg(Global_pos_obj.angles)
            lnpos = Global_pos_obj.ee

            if gang[1]<-200:
               gang[1]=-200
            elif gang[1]>0:
                 gang[1]=0
            Global_pos_obj.angles=np.deg2rad(gang)
            lnpos = Global_pos_obj.ee
            gang1 = Global_pos_obj.angles
            gang =np.rad2deg(Global_pos_obj.angles)

            Global_pos_obj1 = tinyik.Actuator([self.lj1,'x','z',[0,-(self.link1+self.link2+self.end_p),0]])
            Global_pos_obj1.angles = Global_pos_obj.angles
            lnpos1 = Global_pos_obj1.ee
            
            Global_pos_obj2 = tinyik.Actuator([lnpos,'y','x',[lnpos1[0],lnpos1[1],lnpos1[2]]])
            Global_pos_obj2.ee = pos1
            gangs2 = Global_pos_obj2.angles
            gang2 =np.rad2deg(Global_pos_obj2.angles)
            lnpos2 = Global_pos_obj2.ee

            Global_pos_obj3 = tinyik.Actuator([lnpos,'x','z','y','x',[0,-(self.link2+self.end_p),0]])
            Global_pos_obj3.angles = [gang1[0],gang1[1],gangs2[0],0]
            lnpos3=Global_pos_obj3.ee
            #
            eror_pos = self.working_area_cal(pos1,lnpos3)
            i=-1
            eror_pos2=10
             
            for k in range(96):     
                i=i-1
                if eror_pos2>eror_pos[3]:
                    eror_pos2=eror_pos[3]
                else:
                    break
                Global_pos_obj3.angles = [gang1[0],gang1[1],gangs2[0],np.deg2rad(i)]
                lnpos3=Global_pos_obj3.ee
                eror_pos = self.working_area_cal(pos1,lnpos3)
            eror_pos2=1000
            gangs3 = Global_pos_obj3.angles
            if eror_pos[3]>0.005:
                if pos1[1]>lnpos3[1] :
                    i=0
                    for k in range(90):     
                            i=i-1
                            if eror_pos2>eror_pos[3]:
                                eror_pos2=eror_pos[3]
                            else:
                                break
                            Global_pos_obj3.angles = [gang1[0],gang1[1],gangs2[0]+np.deg2rad(i),gangs3[3]]
                            lnpos3=Global_pos_obj3.ee
                            eror_pos = self.working_area_cal(pos1,lnpos3)
                elif pos1[1]<lnpos3[1] :
                    i=0
                    for k in range(90):     
                            i=i+1
                            if eror_pos2>eror_pos[3]:
                                eror_pos2=eror_pos[3]
                            else:
                                break
                            Global_pos_obj3.angles = [gang1[0],gang1[1],gangs2[0]+np.deg2rad(i),gangs3[3]]
                            lnpos3=Global_pos_obj3.ee
                            eror_pos = self.working_area_cal(pos1,lnpos3)
            
            
            gang3 =np.rad2deg(Global_pos_obj3.angles)
            
            eror_pos = self.working_area_cal(pos1,lnpos3)

            rang=True 
            if eror_pos[3]>0.02:
               rang=False
               print(" out of range go to Object ",eror_pos[3])
            if pos1[2]<0.22:
                rang=False
                print(" very close minmum range 0.22 but get",round(pos1[2],2) ," go back the Object", 0.22 - pos1[2])
                
            return [gang[0],gang[1],gang3[2],gang3[3]],lnpos3,rang
          
