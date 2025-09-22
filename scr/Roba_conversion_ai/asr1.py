 
import threading
import time
import numpy as np
import speech_recognition as sr
import IPython.display as ipd
from IPython.display import clear_output

class ASRtext:
    
    def __init__(self):
        
        self.terment=True
        self.indexmic=0
        self.audio=None
        self.text=''
        for i in range(len(sr.Microphone.list_microphone_names())):
            if 'default' == sr.Microphone.list_microphone_names()[i]:
                self.indexmic=i
        self.asrth  =  threading.Thread(target= self.ASR_to_text,daemon=True)
        self.asrth.start()
        
    def ASR_restart(self):
 
         self.audio=None
         self.indexmic=0
         self.terment=False
         time.sleep(4)
         try:
                 self.asrth  =  threading.Thread(target= self.ASR_to_text,daemon=True)
                 self.terment=True
                 self.asrth.start()
                 print("restart")
                
         except:
            print("Error: unable to start thread")
         
    def ASR_to_text(self):

        #global terment
        for i in range(len(sr.Microphone.list_microphone_names())):
            if 'default' == sr.Microphone.list_microphone_names()[i]:
                self.indexmic=i
                
        self.mic = sr.Microphone(device_index= self.indexmic,sample_rate=48000)
        self.r =  sr.Recognizer()
        print("start ASR",self.indexmic)
        c=0
        while self.terment:
                try:
                    clear_output(wait=True)
                    c=c+1
                    print("say ",c," : ")   
                    
                    with  self.mic as source:
                          #self.r.adjust_for_ambient_noise(source,duration=3)
                          self.r.energy_threshold = 300
                          self.r.dynamic_energy_threshold = False
                          self.audio =  self.r.listen(source,timeout=1) #, duration=2abs ,language="en-IN"
                          #self.audio = self.r.record(source)
 
                          self.text = self.r.recognize_google(self.audio,language="en-IN")
                          print(self.get_text())
                          time.sleep(2)
                          
                except:
                    k=0#print("error")
        print("exit thered")
        #ipd.Audio(self.audio.get_wav_data, rate=22050,autoplay=True)
            
    def get_text(self):
        
         return self.text
        
asrs = ASRtext()

