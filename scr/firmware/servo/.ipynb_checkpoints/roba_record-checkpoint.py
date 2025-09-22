import os
import sys
import pickle
import numpy as np
sys.path.insert(1, '/home/roba/Robot_roba/datas/') #path init for find library

class Roba_recoddata:
        
    def __init__(self,pos):
        self.pos=pos
        self.speed={1: 400, 2: 400, 3:4, 4:4, 5: 145, 6: 60,7: 200, 8: 200, 9:4, 10:4, 11: 145, 12: 145,13: 145,14: 145}
        self.stime=0
        self.LF=0
        self.RF=0
        
    def speed_con1(self,pos,c):
        
        if c==4:
            for i in range(1,len(pos)):
                 
                for j in range(1,15):
                    ps=pos[i-1].pos[j]-pos[i].pos[j]
                    if ps<0:
                        ps=ps*-1
                    if j==1 or  j==2 or j==7 or j==8:
                       pos[i].speed[j]=round(ps*5)
                    
                    elif j==5 or j==6 or j==11 or j==12 or j==13 or j==14:
                       pos[i].speed[j]=round(ps*1.25)
                    
                    elif j==3 or j==4 or j==9 or j==10 :
                         pos[i].speed[j]=4
                            
        if c==8:
            for i in range(1,len(pos)):
                 
                for j in range(1,15):
                    ps=pos[i-1].pos[j]-pos[i].pos[j]
                    if ps<0:
                        ps=ps*-1
                    if j==1 or  j==2 or j==7 or j==8:
                       pos[i].speed[j]=ps*10
                    
                    elif j==5 or j==6 or j==11 or j==12 or j==13 or j==14:
                       pos[i].speed[j]=round(ps*2.5)
                    
                    elif j==3 or j==4 or j==9 or j==10 :
                         pos[i].speed[j]=8
                            
        return pos
    def pers(self,v,p):
            per=(v*p)/100
            per=v+per
            return per

    def recon_speed(self,rdatas,per=200):
                posa = np.empty((0, 14), int)
                for i in range(1,len(rdatas)):
                    psr=np.array([])
                    for j in range(1,15):
                        ps = rdatas[i-1].pos[j]-rdatas[i].pos[j]
                        if ps<0:
                            ps=ps*-1
                        psr = np.append(psr,[ps])
                    posa = np.append(posa, np.array([psr]), axis=0)

                posa=posa.astype(int)
                for i in range(len(posa)):
                    n=np.argmax(posa[i])
                    ps=posa[i][n]
                    n=n+1
                    rps=1
                    if n==1 or n==2 or n==7 or n==8:
                       rps=( (6000*ps)/100 )

                    elif n==3 or n==4 or n==9 or n==10:
                       rps=((125*ps)/4)

                    elif n==5 or n==6 or n==11 or n==12:
                       rps=( (1499.4*ps)/80)

                    for j in range(14):
                        poss = posa[i][j]

                        if j==0 or j==1 or j==6 or j==7:

                           if poss==0:
                              rdatas[i+1].speed[j+1]=0
                           else:
                               sp = np.around( (poss*6000)/rps)
                               rdatas[i+1].speed[j+1]=int(self.pers(sp,per)) 

                        elif j==2 or j==3 or j==8 or j==9:
                             if poss==0:
                               rdatas[i+1].speed[j+1]=0
                             else:
                               sp=np.around((poss*125)/rps)
                               rdatas[i+1].speed[j+1]=int(self.pers(sp,per)) 

                        elif j==4 or j==5 or j==10 or j==11 or j==12 or j==13:
                             if poss==0:
                                rdatas[i+1].speed[j+1]=0
                             else:
                               sp=np.around( (poss*1499.4)/rps)
                               rdatas[i+1].speed[j+1]=int(self.pers(sp,per)) 
              
                return rdatas

    def speed_con(self,pos):
        
        
        for i in range(1,len(pos)):
            rp=[]
            lp=[]
            rp=[]
            rps={}
            lpc={}
            rpc={}
            for j in range(1,15):
                 
                    ps=pos[i-1].pos[j]-pos[i].pos[j]
                     
                    if ps<0:
                        ps=ps*-1
                    rp.append(ps)
                    
                    if j==1 or j==2 or j==7 or j==8:
                       rps[j]=( (6000*ps)/100 )
                    
                    elif j==3 or j==4 or j==9 or j==10:
                       rps[j]=((125*ps)/4)
                    
                    elif j==5 or j==6 or j==11 or j==12:
                       rps[j]=( (1499.4*ps)/80)

            
                
            if ( rps[3]>=rps[4] ) and rps[3]!=0:
                if rps[4]!=0:
                    rpc[4]=rps[4]     
                else:
                    rpc[3]=rps[3]
                    
            elif  rps[3]<rps[4] :
                if rps[3]!=0:
                   rpc[3]=rps[3]
                else:
                   rpc[4]=rps[4] 
                
            elif ( rps[1]>=rps[2] ) and rps[1] != 0:
                if rps[2]!=0:
                   rpc[2]=rps[2]
                else:
                    rpc[1]=rps[1]
            elif ( rps[1]<rps[2] ):
                if rps[1]!=0:
                   rpc[1]=rps[1]
                else:
                     rpc[2]=rps[2]
                        
            elif ( rps[5]>=rps[6] ) and rps[5] != 0 :
                if rps[6]!=0:
                   rpc[6]=rps[6]
                else:
                    rpc[5]=rps[5]
            elif ( rps[5]<rps[6] ):
                if rps[5]!=0:
                   rpc[5]=rps[5]
                else:
                   rpc[6]=rps[6]
                
            if ( rps[9]>=rps[10] ) and rps[9] != 0 :
                if rps[10]!=0:
                  lpc[10]=rps[10]   
                else:
                    lpc[9]=rps[9]
            elif ( rps[9]<rps[10] ):
                if rps[9] != 0:
                   lpc[9]=rps[9]
                else:
                  lpc[10]=rps[10]  
                
            elif ( rps[7]>=rps[8] ) and rps[7] != 0 :
                if rps[8] != 0:
                   lpc[8]=rps[8]
                else:
                    lpc[7]=rps[7]
            elif ( rps[7]<rps[8] ):
               
                if rps[7] != 0:
                   lpc[7]=rps[7]
                else:
                    lpc[8]=rps[8]
                
            elif ( rps[11]>=rps[12] ) and rps[11] != 0 :
                if rps[12] != 0:
                   lpc[12]=rps[12]
                else:
                    lpc[11]=rps[11]
            elif ( rps[11]<rps[12] ):
                if rps[11] != 0:
                   lpc[11]=rps[11]   
                else:
                    lpc[12]=rps[12]
            
             
            for j in range(1,15):
                
                if j <=6:
                    rd=0
                    for d in rpc:
                        rd=d
                    if len(rpc)>=1:
                        
                        if j==1 or  j==2  :
                           #print(rpc[rd] ,rd )
                           sp = round( (rp[j-1]*6000)/rpc[rd])
                           if sp>800:
                              pos[i].speed[j]=400
                           else:
                              pos[i].speed[j]=sp

                        elif j==5 or j==6 :
                           sp=round( (rp[j-1]*1499.4)/rpc[rd] )
                           if sp>500:
                                pos[i].speed[j]=200
                           else:
                              pos[i].speed[j]=sp

                        elif j==3 or j==4 :
                             sp=round((rp[j-1]*125)/rpc[rd])
                             if sp>20:
                                pos[i].speed[j]=15
                             else:
                                pos[i].speed[j]=sp
 
                else:
                    rd=0
                    for d in lpc:
                        rd=d
                    if len(lpc)>=1:
                        if j==7 or j==8:
                            #print(lpc ,i)
                            sp =round( (rp[j-1]*6000)/lpc[rd])
                            if sp>800:
                              pos[i].speed[j]=400
                            else:
                              pos[i].speed[j]=sp

                        elif j==11 or j==12 or j==13 or j==14 :
                           sp=round( (rp[j-1]*1499.4)/lpc[rd] )
                           if sp>500:
                                pos[i].speed[j]=200
                           else:
                              pos[i].speed[j]=sp

                        elif j==9 or j==10:
                                 # print(rd)
                                 # print(lpc[rd],rd)
                                 sp=round((rp[j-1]*125)/lpc[rd])
                                 if sp>20:
                                    pos[i].speed[j]=15
                                 else:
                                    pos[i].speed[j]=sp
                            
         
        return pos
    
    def save(self,data):
       with open('/home/roba/Robot_roba/datas/roba_data15.roba', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    def get_data(self):
         self.robadata=[]
         with open('/home/roba/Robot_roba/datas/roba_data8.roba', 'rb') as roba_face_model:
              self.robadata=pickle.load(roba_face_model)
         return self.robadata