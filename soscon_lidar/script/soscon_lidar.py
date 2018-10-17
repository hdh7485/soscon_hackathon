#!/usr/bin/env python
import sys
import rospy
import socket
import array
import math
import time
import pickle

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class socket_linker:

    def __init__(self, host, port, data_size):
        
        rospy.init_node('lidar_publisher')
        self.host = host
        self.port = port
        self.data_size = data_size
        
        self.server_address = (host, port)
        self.connect()
        
        self.pub = rospy.Publisher('scan', LaserScan, queue_size=50)
        self.twist_pub = rospy.Publisher('twist', Twist, queue_size=50)
        self.rate = rospy.Rate(20)

        self.num_readings = 360
        self.laser_frequency = 20.
        self.ranges = [0] * self.num_readings
        self.intensities = [0] * self.num_readings

        self.rate = rospy.Rate(10)


    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.sock.connect(self.server_address)
                print("connected")
                break
            except Exception as e:
                print("cannot connect")
		break

    def rec_lidar(self):
        #Receive lidar data
        self.receive_data = self.sock.recv(self.data_size)
        if not self.receive_data:
            print("broken connection")
            self.disconnect()
        # print("length of rdata :",len(self.receive_data))
        zipped_data = pickle.loads(recvd_data)
        lidar_data = zipped_data[0]
        delta_x_data = zipped_data[1]
        delta_y_data = zipped_data[2]
        compass_data = zipped_data[3]
        print(delta_x_data)

    def disconnect(self):
        print("disconnect")
        self.sock.close()
        sys.exit()

    def shuthook (self):
        self.disconnect()
        print ("shutdown")

if __name__== '__main__':
    print("start")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.27.4', 10000))
    rospy.loginfo("connected")
    while not rospy.is_shutdown():
        recvd_data = sock.recv(3600)
        print(recvd_data)
        zipped_data = pickle.loads(recvd_data)
        lidar_data = zipped_data[0]
        delta_x_data = zipped_data[1]
        delta_y_data = zipped_data[2]
        compass_data = zipped_data[3]
        print(compass_data)
    sock.close()

    #while not rospy.is_shutdown():
        #receive_data = sock.recv(360*10)
        #if not receive_data:

    #while not rospy.is_shutdown():
        #pass
        # time.sleep(0.05)
        #sock.rec_lidar()
        # sock.rec_delta()

