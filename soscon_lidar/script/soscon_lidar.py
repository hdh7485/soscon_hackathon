#!/usr/bin/env python
import sys
import rospy
import socket
import array
import math
import time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class socket_linker:

    def __init__(self, host, port, data_size):

        rospy.init_node('lidar_publisher')
        self.host = host
        self.port = port
        self.data_size = data_size
        self.server_address = (host, port)
        self.connect()
        self.pub_lidar = rospy.Publisher('scan', LaserScan, queue_size=1)
        self.pub_delta = rospy.Publisher('delta', Twist, queue_size=1)
        self.num_readings = 360
        self.laser_frequency = 20.0
        self.ranges = [0] * self.num_readings
        self.intensities = [0] * self.num_readings
   
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.sock.connect(self.server_address)
                print 'connected'
                break
            except Exception as e:
                print 'cannot connect'

    def rec_data(self):
        try:
            self.rdata = self.sock.recv(self.data_size)
            if not self.rdata:
                print 'broken connection'
                self.disconnect()
            print ('length of rdata :', len(self.rdata))
            rospy.loginfo('rec_data')
            scan = LaserScan()
            scan.header.frame_id = 'laser'
            scan_time = rospy.Time.now()
            scan.header.stamp = scan_time
            scan.angle_min = 0
            scan.angle_max = 2 * math.pi
            scan.angle_increment = 6.28 / self.num_readings
            scan.time_increment = 1 / self.laser_frequency / self.num_readings
            scan.range_min = 0.2
            scan.range_max = 6.0
            self.ldata = list(array.array('f', self.rdata))
            
            delta = Twist()
            delta.angular.z = self.ldata.pop()
            delta.linear.y = self.ldata.pop()
            delta.linear.x = self.ldata.pop()

            print ('length of ldata :', len(self.ldata))
            for i in reversed(range(self.num_readings)):
                scan.ranges.append(self.ldata[i] / 100.0)

            self.pub_data_lidar(scan)
            self.pub_data_delta(delta) 

        except Exception as ex:
            print ('Exception in rec_data', ex)
            self.disconnect()

    def pub_data_delta(self, data):
        rospy.loginfo('publish delta')
        self.pub_delta.publish(data)

    def pub_data_lidar(self, data):
        rospy.loginfo('publish lidar')
        self.pub_lidar.publish(data)

    def disconnect(self):
        print 'disconnect'
        self.sock.close()
        sys.exit()

    def shuthook(self):
        self.disconnect()
        print 'shutdown'


if __name__ == '__main__':
    sock = socket_linker('52.193.18.72', 10004, 5772)
    while not rospy.is_shutdown():
        time.sleep(0.05)
        sock.rec_data()
