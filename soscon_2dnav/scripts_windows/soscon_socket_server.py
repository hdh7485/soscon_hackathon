import socket
import sys
from soscon.env import Env
from soscon.status import Status
import array

import numpy as np
import time
import math

import socket
from _thread import *
from threading import Thread

class data_ob:
    
    def __init__(self):
        self.env = Env()
        self.env.on_observation = self.on_observation
#         self.frame_rate = 20
        self.delay = 0.05
    
    def on_observation(self, observation, status_code):
#         self.ir = observation.ir
#         self.encoder = observation.encoder
        self.lidar = observation.lidar
#         self.boundingbox = observation.boundingbox
#         self.robot_location = observation.robot_location
        self.delta = observation.delta
        self.compass = observation.compass
        
class server_soc:
    
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        
    def connect(self):
        self.connection, self.client_address = self.sock.accept()
        print(sys.stderr, 'connecting from', self.client_address)

def send_msg(connection, data):
    while True:
        try:
            print("start")
            x = data.lidar
            x.append(data.delta.x)
            x.append(data.delta.y)
            x.append(data.compass)
            connection.sendall(array.array('f', x))
            time.sleep(data.delay)
        except Exception as e:
            print("error--->",e)

# In[2]:


if __name__ == '__main__':

    
    try:
        
        test = server_soc('0.0.0.0',10004)
        ureal = data_ob()
        test.connect()
        #while True:
        #    time.sleep(0.01)
        print("server connected")

    except Exception as e:
        print("connection error", e)
        test.connection.close()
        
    try:   
        start_new_thread(send_msg, (test.connection,ureal))
        #start_new_thread(recv_msg, (test.connection,))
        print("thread on")

    except Exception as e:
        print("thread error",e)
        test.connection.close()


# In[ ]:




