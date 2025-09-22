import threading
import time

class tst:
     def __init__(self):
        self.text="far"
        self.thc=0
        
     def lp(self,bar):
          for i in range(50):
                time.sleep(0.3)
                t= bar+" "+str(i)
                b=t
          return b       
     def tg(self,bar,tc):
            ct = self.lp(bar)
            if tc==self.thc:
               self.text=ct
     def tsb(self,bar,tc):
            self.thc=tc
            gth = threading.Thread(target=self.tg, args = (bar,tc, ),daemon=True)
            gth.start()
     def rt(self):
          return self.text