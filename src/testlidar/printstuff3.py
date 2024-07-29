#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
def callback(data):
    #print(type(list(data)))
    ranges = (data.ranges)
    m = min(ranges)
    print(m, ranges.index(m), ranges.index(m)/len(ranges))
    #rospy.loginfo("Received lidar data: %s", data)
def listener():
    rospy.init_node('lidar_listener', anonymous=True)
    rospy.Subscriber('/velodyne/scan', LaserScan, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
