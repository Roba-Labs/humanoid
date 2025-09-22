import time
import serial
class wheel:
        def __init__(self,com):
            self.roba_connection = serial.Serial()
            self.roba_connection.baudrate = 115200
            self.roba_connection.port = com
            #self.roba_connection.timeout = 0.5
            self.roba_connection.open()
            #self.roba_connection.timeout(2.0)
            self.lastdata=' '
            time.sleep(1)
        # send data to ardiuno
        def send_data(self,data):
            if (self.roba_connection.is_open):
                self.lastdata=" "
                self.roba_connection.write(data.encode())
                while True:
                    v = self.roba_connection.readline().decode()
                    self.lastdata=self.lastdata+v
                    vs =set(v.split())
                    if (vs & {'off'} ) == {'off'}:
                        break
        def send_data_only(self,data):
            if (self.roba_connection.is_open):
                #self.lastdata=""
                self.roba_connection.write(data.encode())
                 
        # read data from arduino
        def read_all(self):
             if (self.roba_connection.is_open):
                 return self.roba_connection.read_all().decode()
                 
        def close_S(self):
            self.roba_connection.close()
        
        def get_mv(self, mv):
            return str(mv[0])+" "+str(mv[1])+" "+str(mv[2])+" "+str(mv[3])

        def forward1(self,mv):
            data = "{mv:[50,0,0,"+str(mv)+"]}"
            self.send_data_only(data)
        def backward1(self,mv):
            data = "{mv:[0,"+str(mv)+",50,0]}"
            self.send_data_only(data)
        def left(self):
            self.send_data_only("{mv:[40,0,40,0]}")  
        def right(self):
            self.send_data_only("{mv:[0,40,0,40]}") 
        def stop(self):
            self.send_data_only("{mv:[0,0,0,0]}")

        def forward(self,mv):
            data = "{mv:["+str(mv[0])+",0,0,"+str(mv[1])+"]}"
            self.send_data_only(data)

        def backward(self,mv):
            data = "{mv:[0,"+str(mv[0])+","+str(mv[1])+",0]}"
            self.send_data_only(data)

        def mright(self,mv):
            data = "{mv:[0,"+str(mv)+",0,"+str(mv)+"]}"
            self.send_data_only(data)
                
        def mleft(self,mv):
              data= "{mv:["+str(mv)+",0,"+str(mv)+",0]}"
              self.send_data_only(data)