#from soscon.data.observation import Observation
import socket
import sys
from soscon.env import Env
from soscon.status import Status
import array
import numpy as np
import time
import pickle

class data_ob:
    def __init__(self):
        self.env = Env()
        self.env.on_observation = self.on_observation
        self.frame_rate = 20
        self._event_timer_delay = 1 / self.frame_rate
    
    def on_observation(self, observation, status_code):
        self.ir = observation.ir
        self.encoder = observation.encoder
        self.lidar = observation.lidar
        self.boundingbox = observation.boundingbox
        self.delta = observation.delta
        self.compass = observation.compass
        # print(self.delta.x)
        # lidar_data = [float(i) for i in ureal.lidar]
        # lidar_data = ureal.lidar
        # delta_data = ureal.delta
        # compass_data = ureal.compass
        # print([self.lidar, self.delta.x, self.delta.y, self.compass])
        
class server_soc:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)
        self.sock.bind(self.server_address)
        self.sock.listen(1)

    def connect(self):
        self.connection, self.client_address = self.sock.accept()
        print(sys.stderr, 'connecting from', self.client_address)

if __name__ == '__main__':
    server = server_soc('',11411)
    ureal = data_ob()
    print(ureal)

    while True:
        print(sys.stderr,'waiting for a connection')
        server.connect()
        try:
            print('connected')
            while True:
                # print(ureal.delta)
                print([self.lidar, self.delta.x, self.delta.y, self.compass])
                send_data = pickle.dumps([self.lidar, self.delta.x, self.delta.y, self.compass])
                server.connection.sendall(send_data)

                # server.connection.sendall(array.array('f',ureal.lidar))
                # server.connection.sendall(ureal.delta)
                # server.connection.sendall(ureal.compass)
                time.sleep(ureal._event_timer_delay)
        except socket.error as er:
            server.connection.close()
            print('disconnected')