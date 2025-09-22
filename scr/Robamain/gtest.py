import sys
sys.path.insert(1, '/home/roba/Robot_roba/scr/Robamain')  
sys.path.insert(1, '/home/roba/Robot_roba/scr/Roba_conversion_ai')  
sys.path.insert(1, '/home/roba/Robot_roba/scr/Roba_vision')  
sys.path.insert(1, '/home/roba/Robot_roba/scr/firmware/servo')  
import ASR
import robaaibot
import threading
import time
import Speak2rpi
 
class RobaMain:
      
      def __init__(self):
          
            self.robaAIC = robaaibot.RobaBot()
            time.sleep(0.2)
            self.spk = Speak2rpi.speak("192.168.0.120")
            self.spk.recev_data="Pause"
            time.sleep(0.2)
            self.asrs = ASR.ASRtext()
            self.CAIb=True
             
      def init_CAI(self):
            playtim=0
            global anstext
            while self.CAIb:
                    textq=""
                    time.sleep(0.2)
                    self.asrs.rcvdata=self.spk.recev_data2
                    playtim=playtim+1
                    if playtim>=70:
                        playtim=0
                        self.asrs.terment=False
                        self.asrs.ASR_restart()
                        self.spk.recev_data=="Pause"
                        self.asrs.microph=True
                    
                    if self.spk.recev_data=="Pause":
                        playtim=0
                        self.asrs.microph=True
                        if not self.asrs.asrth.isAlive():
                               self.asrs.ASR_restart()
                        textq = self.asrs.get_text()
                        if textq =='' and textq ==" ":   
                            textq="&"
                        if textq !="&":
                           self.asrs.clear_text()
                           self.asrs.microph=False
                            
                           anstext= self.robaAIC.get_ans(textq) 
                           
                           textq="&"
                           anstext = str(anstext)
                           if len(anstext)>1 and anstext != "['']" and anstext !='' and anstext !=" ":                                       
                                start_time = time.time()
                                self.asrs.microph=False
                                self.asrs.clear_text()
                                self.spk.Speaking(anstext)
                                self.asrs.thcn=self.asrs.thcn+1
                                self.asrs.clear_text()
                                while time.time() - start_time <1:
                                        self.asrs.microph=False
                                        self.asrs.thcn=self.asrs.thcn+1
                                        self.asrs.clear_text()
                                        time.sleep(0.01)
 
                           else:
                                self.spk.recev_data="Pause"
                                self.asrs.microph=True
                           self.asrs.clear_text()
                    else:
                        self.asrs.microph=False
                        self.asrs.clear_text()
                        
            print("exit CAI")
            
def main():
    roba =RobaMain()
    time.sleep(0.2)
    roba.spk.recev_data="Pause"
    CAIT  =  threading.Thread(target= roba.init_CAI,daemon=True) 
    CAIT.start()
    print("start roba")
if __name__ == "__main__":
    main()