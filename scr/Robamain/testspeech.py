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
            self.CAIb=True
            self.asrs = ASR.ASRtext()
            
      def init_CAI(self):
            playtim=0
            global anstext
            while True:
                 try:
                        time.sleep(0.2)
                        """
                        textq=""
                        time.sleep(0.2)
                        playtim=playtim+1
                        if playtim>=70:
                            playtim=0
                            self.asrs.terment=False
                            self.asrs.ASR_restart()
                            self.spk.recev_data=="Pause"
                            self.asrs.microph=True

                        if not self.asrs.asrth.isAlive():
                               self.asrs.ASR_restart()
                               self.asrs.microph=True

                        else:
                            textq = self.asrs.get_text()
                            if textq =='' and textq ==" ":   
                                textq="&"
                            if textq !="&":
                               self.asrs.thcn=self.asrs.thcn+1
                               print(textq)
                               self.asrs.clear_text()
                               textq="&"
                        """
                        print("error init_CAI",self.asrs.enter )
                 except:
                    print("error init_CAI",self.asrs.enter )
                         
            print("exit CAI")
            
def main():
    roba =RobaMain()
    time.sleep(0.2)
    CAIT  =  threading.Thread(target= roba.init_CAI,daemon=True) 
    CAIT.start()
    print("start roba")
if __name__ == "__main__":
    main()