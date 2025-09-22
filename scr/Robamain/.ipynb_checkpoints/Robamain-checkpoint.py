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
            self.spk.recev_data="Paused"
            time.sleep(0.2)
            
            self.CAIb=True
             
      def init_CAI(self):
            playtim=0
            self.asrs = ASR.ASRtext()
            global anstext
            while self.CAIb:
                    textq=""
                    time.sleep(0.2)

                    #playtim=playtim+1
                    # if playtim>=70:
                    #     playtim=0
                    #     self.asrs.terment=True
                    #     self.asrs = ASR.ASRtext()
                    #     self.spk.recev_data=="Pause"
                    #     self.asrs.microph=True
                    #print(self.spk.recev_data , self.spk.recev_data2)
                    if self.spk.recev_data=="Paused":
                        playtim=0
                        textq = self.asrs.get_text()
                        
                        if textq =='' and textq ==" ":   
                            
                            textq="&"
                            self.asrs.clear_text()
                            self.asrs.microph=True
                            
                        if textq !="&" and len(textq)>1 and textq != "['']" and textq !='' and textq !=" ":
                           self.asrs.clear_text()
                           print(textq)
                           anstext= self.robaAIC.get_ans(textq) 
                           textq="&"
                           anstext = str(anstext)
                           if len(anstext)>1 and anstext != "['']" and anstext !='' and anstext !=" ":                                       
                                self.spk.Speaking(anstext)
                                start_time = time.time()
                                
                                while self.spk.recev_data !="Playing":
                                        time.sleep(0.1)
                                        if  time.time() - start_time>5:
                                            break
                                start_time = time.time()
                                while self.spk.recev_data !="Paused":
                                        self.asrs.microph=False
                                        time.sleep(0.1)
                                        if  time.time() - start_time>10:
                                            break
                                self.asrs.microph=True
                                time.sleep(1.5)
                                self.asrs.clear_text()
                                
                        else:
                           self.asrs.microph=True
                           self.asrs.clear_text()
                           

            print("exit CAI")
            
def main():
    roba =RobaMain()
    time.sleep(0.2)
    roba.spk.recev_data="Paused"
    CAIT  =  threading.Thread(target= roba.init_CAI,daemon=True) 
    CAIT.start()
    print("start roba")
if __name__ == "__main__":
    main()