#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
def callback(data):
    #print(type(list(data)))

    ranges = (data.ranges)
#    backind = 0
#    rightind = len(data.ranges)//4
#    frontind = len(data.ranges)//2
#    leftind = (3*len(data.ranges))//4
    leftind = (2*len(ranges))//3
    rightind = len(ranges)//3
    frontind = len(data.ranges)//2
    print(rightind, leftind)
    mmWave = data.ranges[rightind:leftind+1][::-1][:300]

    print(len(mmWave)/len(data.ranges))


    print('\n'.join(str(i) for i in mmWave))
    print(f'left = {round(data.ranges[leftind],2)}, front = {round(data.ranges[frontind],2)}, right = {round(data.ranges[rightind],2)}')

    #m = min(ranges)


    #print(m, ranges.index(m), ranges.index(m)/len(ranges))
    #rospy.loginfo("Received lidar data: %s", data)
def listener():
    rospy.init_node('lidar_listener', anonymous=True)
    rospy.Subscriber('/velodyne/scan', LaserScan, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
