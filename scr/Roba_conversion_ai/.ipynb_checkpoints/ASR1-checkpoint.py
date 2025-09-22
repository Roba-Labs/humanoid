 
import threading
import time
import numpy as np
import speech_recognition as sr
import IPython.display as ipd
from IPython.display import clear_output
import soundcard as sc

class ASRtext:
    
    def __init__(self):
        global gt
        self.gt=True
        self.microph=True
        self.rcvdata="no"
        sc.all_microphones()
        time.sleep(2)
        self.terment=True
        self.enter=False
        self.indexmic=0
        self.audio=None
        self.text="&"
        self.asrth=None
        self.thcn=0
        self.smc = sr.Microphone.list_microphone_names()
        self.r =  sr.Recognizer()
        
        for i in range(len(self.smc)):
            try:
                    print(self.smc[i])
                    if 'GS3: USB Audio (hw:2,0)'== self.smc[i]:
                        self.indexmic=i
                        break
                    elif 'default' == self.smc[i]:
                         self.indexmic=i
                         
            except:
                pass
        self.asrth  =  threading.Thread(target= self.ASR_to_text,daemon=True)
        self.asrth.start()
        
    def ASR_restart(self):
         self.thcn=0
         global gt
         self.gt=True
         self.microph=True
         self.audio=None
         self.indexmic=0
         self.terment=False
         time.sleep(4)
         try:    
                 self.terment=True
                 self.asrth  =  threading.Thread(target= self.ASR_to_text,daemon=True)
                 self.asrth.start()
                 print("restart")
                
         except:
            print("Error: unable to start thread")
         
    def google_ASR(self,audio,rec,tcs):
           global gt
           self.gt=False
           try:
                 
                tdata = rec.recognize_google(audio,language="en-IN")
                if tcs==self.thcn:
                    self.text=tdata
                    #self.microph=False
                else:
                    self.text="&"
                    self.gt=True
           except:
             h=0
             self.text="&"
        
            
    def ASR_to_text(self):
        self.text="&"
        
        #global terment
        self.smc = sr.Microphone.list_microphone_names()
        for i in range(len(self.smc)):
            try:
                    if 'GS3: USB Audio (hw:2,0)'== self.smc[i]:
                        self.indexmic=i
                        break
                    elif 'default' == self.smc[i]:
                         self.indexmic=i
                            
            except:
                pass
        
        global gt
        print("start ASR",self.indexmic)
        c=0
        g=0
        print(self.gt)
        self.mic = sr.Microphone(device_index= self.indexmic,sample_rate=48000)
        start = time.time()
        time.sleep(1)
        self.enter=True
        while self.terment:
                       
                        time.sleep(0.1)
                         
                        print("say ",self.thcn," ",self.microph) 
                        if self.microph:
                                #and  (self.text =="&" or len(self.text)<2 or self.text == "['']" or self.text =='' or self.text ==" " ) :
                            #c=c+1
                            
                            self.r =  sr.Recognizer()
                            with  self.mic as source:

                                    try:
                                          #self.r.adjust_for_ambient_noise(source,duration=8)
                                          self.r.energy_threshold = 500
                                          self.r.dynamic_energy_threshold = False
                                          self.audio =  self.r.listen(source,timeout=3,phrase_time_limit=3)
                                          #self.audio = self.r.record(source)
                                          #print(self.gt)
                                          end = time.time() - start
                                          if self.microph:
                                              if(self.gt or end>9):

                                                   self.thcn=self.thcn+1
                                                   start = time.time()
                                                   gth = threading.Thread(target=self.google_ASR, args = (self.audio,self.r,self.thcn, ),daemon=True)
                                                   gth.start()

                                    except:
                                        k=0
              
                        else:
                            # time.sleep(0.3)
                            # self.thcn=self.thcn+1
                            self.text="&"
                             

        print("exit thered")

  
    def get_text(self):
         return self.text
    def clear_text(self):
           self.text="&"