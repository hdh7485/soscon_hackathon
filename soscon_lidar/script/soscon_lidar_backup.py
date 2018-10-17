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

    # def rec_compass(self):
    #     try:
    #         #Receive delta data
    #         self.compass_data = self.sock.recv(self.data_size)
    #         if not self.delta_data:
    #             print("broken connection")
    #             self.disconnect()

    #         rospy.loginf("Receive twist data")
    #         odom = Odometry()

    #         odom.pose.pose.Quaternion = compass_data

    #         rospy.loginfo("publish twist data")
    #         self.twist_pub.publish(twist)

    #     except Exception as ex:
    #         print("Exception in twist_data", ex)
    #         self.disconnect()

    # def rec_delta(self):
    #     try:
    #         #Receive delta data
    #         self.delta_data = self.sock.recv(self.data_size)
    #         if not self.delta_data:
    #             print("broken connection")
    #             self.disconnect()
    
    #         rospy.loginf("Receive twist data")
    #         odom = Odometry()

    #         odom.twist.linear.x = delta_data[0]
    #         odom.twist.linear.y = delta_data[1]

    #         rospy.loginfo("publish twist data")
    #         self.twist_pub.publish(twist)

    #     except Exception as ex:
    #         print("Exception in twist_data", ex)
    #         self.disconnect()   

    def rec_lidar(self):
        try:
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

            print(compass_data)
'''

            rospy.loginfo("rec_data")
            scan = LaserScan()
             
            scan.header.frame_id = 'laser'
            scan_time = rospy.Time.now()
            scan.header.stamp = scan_time
            scan.angle_min = 0
            scan.angle_max = 2 * math.pi
            #scan.angle_min = -math.pi
            #scan.angle_max = math.pi
            scan.angle_increment = 6.28 / self.num_readings
            #scan.angle_increment = 1 * (math.pi / 180)
            scan.time_increment = 1 / self.laser_frequency / self.num_readings
            scan.range_min = 0.2
            scan.range_max = 6.
            self.ldata = list(array.array('f',self.rdata))
            
            print("length of ldata :",len(self.ldata))
            #print(self.ldata)
            '''

            '''
            for i in range(self.num_readings-1,0,-1):
                scan.ranges.append(self.ldata[i]/100.)
            '''

            '''
            for i in reversed(range(self.num_readings)):
                scan.ranges.append(self.ldata[i]/100.)

            rospy.loginfo("publish lidar data")
            self.pub.publish(scan)
            #self.rate.sleep()
                
        except Exception as ex:
            print("Exception in rec_lidar", ex)
            self.disconnect()   
            '''

    def pub_data(self, data):
        rospy.loginfo("publish data")
        self.pub.publish(data)
        self.rate.sleep()

    def disconnect(self):
        print("disconnect")
        self.sock.close()
        sys.exit()
    def shuthook (self):
        self.disconnect()
        print ("shutdown")

if __name__== '__main__':
    sock = socket_linker('192.168.24.203',10101,360*4*4)
    while not rospy.is_shutdown():
        time.sleep(0.05)
        sock.rec_lidar()
        # sock.rec_delta()
