import sys
sys.path.insert(1, '/home/roba/Robot_roba/scr/Roba_vision/')
import socket, cv2, pickle,struct,imutils

class ProcessData:
    def __init__(self, data= 'farid'):
           self.data = data

class Ipcam:
        def __init__(self,ip="192.168.0.107"):
                # Socket Create
                global client_socket
                self.client_socket=None
                self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                #host_name  = socket.gethostname()
                self.host_ip =ip  #socket.gethostbyname(host_name)
                print('HOST IP:',self.host_ip)
                self.port = 9999
                self.socket_address = (self.host_ip,self.port)
                # Socket Bind
                self.server_socket.bind(self.socket_address)
                # Socket Listen
                self.server_socket.listen(1)
                print("LISTENING AT:",self.socket_address)

                # Socket Accept
        def stopserver(self):
                 self.server_socket.close()
                 print("Close server ")
        def runserver(self):
                global client_socket
                self.client_socket,self.addr = self.server_socket.accept()
                print('GOT CONNECTION FROM:',self.addr)
        def sendimg(self,img):
        
            img = imutils.resize(img,width=840)
            a = pickle.dumps(img)
            message = struct.pack("Q",len(a))+a
            self.client_socket.sendall(message)
         
        def recvdata(self):
            data_variable="farid"
            data="tst"
             #try:
            data = b""
            payload_size = struct.calcsize("Q")
            while len(data) < payload_size:
                packet = self.client_socket.recv(1024) # 4K
                if not packet: break
                data+=packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(1024)
             
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            #ProcessData("farid")
            data_variable = pickle.loads(frame_data)
#              except:
#                 data_variable="error"
                
            return data_variable

#         def recvdata(self):
#              data_variable="farid"
#              data="tst"
#              try:
#                 data = self.client_socket.recv(4096)
#                 data_variable = pickle.loads(data)
#              except:
#                 data_variable=data
                
#              return data_variable
                
                 
                          