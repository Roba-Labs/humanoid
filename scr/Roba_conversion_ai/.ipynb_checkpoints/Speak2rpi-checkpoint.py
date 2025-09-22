import socket
from threading import Thread
import time
from IPython.display import clear_output
import re
class speak:
    def receving_d(self):
        while(self.breakloop):
            try:
                  time.sleep(0.01)
                  rcdata= self.s.recv(1024) 
                  rcdata = re.split(' |\'|\b',str(rcdata))
                  self.recev_data2=rcdata
                  if  rcdata[1]=='Playing' or  rcdata[1]=='Paused':
                     self.recev_data=  rcdata[1]
                     if   rcdata[1]=="Playing":
                        self.net_conectch=0;
                        self.audio_len= "Playing"
                     else:
                         self.audio_len=0
            except:
                pass

    def __init__(self,ipa):
        self.breakloop=True
        self.breakloop1=False
        self.recev_data="Paused"
        self.recev_data2="of"
 
        self.audio_len=0
        self.net_conectch=0
        self.HOST = '192.168.0.120'
        self.PORT = 13500  
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))
        self.th = Thread(target=self.receving_d)
        self.th.start()
        print("thret start")
        
    def ck(self):
        return self.HOST

    def paly_song(self,com):
 
               try:
                    sc = len(com)
                    scq = "{'cmd':'song','ln':0}"
                    time.sleep(0.1)
                    self.s.sendall(str.encode(scq))
                    time.sleep(0.1)
                    self.s.sendall(str.encode(com))
               except:
                        self.s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.s.connect((self.HOST, self.PORT))
                        sc = len(com)
                        scq = "{'cmd':'song','ln':0}"
                        time.sleep(0.1)
                        self.s.sendall(str.encode(scq))
                        time.sleep(0.1)
                        self.s.sendall(str.encode(com))   
 

    def Speaking(self,com):
 
                try:
                    sc = len(com)
                    scq = "{'cmd':'ttsc','ln':" +str(sc)+"}"
                    time.sleep(0.1)
                    self.s.sendall(str.encode(scq))
                    time.sleep(0.1)
                    self.s.sendall(str.encode(com))
                except:
                        self.s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.s.connect((self.HOST, self.PORT))
                        sc = len(com)
                        scq = "{'cmd':'ttsc','ln':" +str(sc)+"}"
                        time.sleep(0.1)
                        self.s.sendall(str.encode(scq))
                        time.sleep(0.1)
                        self.s.sendall(str.encode(com))
 
 