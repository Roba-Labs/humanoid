import threading
import time
import numpy as np
import speech_recognition as sr
import IPython.display as ipd
from IPython.display import clear_output
import soundcard as sc

class ASRtext:
    
    def get_text(self):
         return self.ttsdata
    def clear_text(self):
           self.ttsdata="&"
    def ASR_to_text(self):
       
        for i in range(len(self.smc)):
            try:
                #print(self.smc[i])
                if "USB Audio Device: - (hw:2,0)"== self.smc[i]:
                    self.indexmic=i
                    break
                elif 'default' == self.smc[i]:
                     self.indexmic=i
            except:
              pass
        print("start ASR", self.indexmic)

        mic = sr.Microphone(device_index= self.indexmic,sample_rate=48000)  
        start = time.time()
        time.sleep(1)
        r =  sr.Recognizer()
        print("say ",self.microph)
        while self.terment:
                clear_output(True)
                time.sleep(0.1)   
                #print("say ",self.microph)
                if self.microph:
                    with mic as source:
                           try:
                                  r.energy_threshold = 500
                                  r.dynamic_energy_threshold = True
                                  audio = r.listen(source,timeout=4,phrase_time_limit=5)
                                  tdata = r.recognize_google(audio)#,language="en-IN"
                                  if len(tdata)>1 and tdata!='' and tdata !=" ":
                                     self.ttsdata=tdata
                                     self.microph=False
                           except:
                                pass

        print("exit thered")
        
        
    def __init__(self):
        self.indexmic=0
        self.microph=True
        self.rcvdata="no"
        sc.all_microphones()
        self.smc = sr.Microphone.list_microphone_names()
        self.r =  sr.Recognizer()
        self.terment=True
        self.ttsdata=" "
        self.asrth  =  threading.Thread(target= self.ASR_to_text,daemon=True)
        self.asrth.start()
        
   