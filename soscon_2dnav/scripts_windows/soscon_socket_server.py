#!/usr/bin/env python
# coding: utf-8

# In[1]:


#from soscon.data.observation import Observation
from IPython.display import clear_output
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
        x = data.lidar
        x.append(data.delta.x)
        x.append(data.delta.y)
        x.append(data.compass)
        connection.sendall(array.array('f', x))
        time.sleep(data.delay)


# In[2]:


if __name__ == '__main__':

    
    try:
        
        test = server_soc('localhost',10000)
        ureal = data_ob()
        test.connect()
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




