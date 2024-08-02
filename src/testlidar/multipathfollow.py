#!/usr/bin/env python
from scipy.signal import savgol_filter as sgf, find_peaks as fp

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan

import rospy
from geometry_msgs.msg import Twist
import time

def move_robot(linear_velocity, angular_velocity):
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    velocity_message = Twist()
    velocity_message.linear.x = linear_velocity
    velocity_message.angular.z = angular_velocity
    #rate = rospy.Rate(200)  # 10 Hz
    velocity_publisher.publish(velocity_message)
    #rate.sleep()

    # Stop the robot after the duration
    #velocity_message.linear.x = 0
    #velocity_message.angular.z = 0
    #velocity_publisher.publish(velocity_message)



def callback(data):
    #print(type(list(data)))
    W_MAX = 0.7
    V_MAX = 0.3
    ranges = (data.ranges)
#    backind = 0
#    rightind = len(data.ranges)//4
#    frontind = len(data.ranges)//2
#    leftind = (3*len(data.ranges))//4
    leftind = (2*len(ranges))//3
    rightind = len(ranges)//3
    frontind = len(data.ranges)//2
    #print(rightind, leftind)
    mmWave = [i if i!=float('inf') else 0 for i in data.ranges[rightind:leftind+1][::-1][:300]]

    #assert len(mmWave)==300
    mmWave = sgf(sgf(mmWave,13,5),13,5)
    print('\n'.join(str(i) for i in mmWave))
    #print(fp(mmWave, height=2.5, distance=60))
    peaks = [*fp(mmWave, height=2.5, distance=60)[0]]
    #if np.sign(np.diff(mmWave))[0] < 0 and mmWave[0] > 2:
    #    peaks = [0] + peaks
    #if np.sign(np.diff(mmWave))[-1] > 0 and mmWave[-1] > 2:
    #    peaks = peaks + [299]
#    print('peaks', [0.401 * (i-150) for i in peaks])
    #print(peaks)
    newpeaks = []
    for x in peaks:
        leftbad = abs((mmWave[x]-mmWave[max(0,x-25)])/mmWave[x])>.6 and mmWave[max(0,x-25)]<4
        rightbad = abs((mmWave[x]-mmWave[min(299,x+25)])/mmWave[x])>.6 and mmWave[min(299,x+25)]<4
        #print(0.4*(x-150), leftbad, rightbad)
        if(leftbad and not rightbad):
            newpeaks.append(min(299,x+60))
        elif(rightbad and not leftbad):
            newpeaks.append(max(0, x-60))
        elif(not rightbad and not leftbad):
            newpeaks.append(x)

    
    peaks = [0.401 * (x-150) for x in newpeaks]
    if not peaks:
        toFollow = 180
        w = W_MAX
        v = 0
    else:
        toFollow = min(peaks)
        w = W_MAX * (-toFollow)/60
        v = V_MAX * (60 - abs(toFollow))/60
    #print('x', x, 'realx', realx)
    print(f'left = {round(data.ranges[leftind],2)}, front = {round(data.ranges[frontind],2)}, right = {round(data.ranges[rightind],2)}')
    print('peaks', peaks)
    print('following', toFollow, '\nv = ', v, '\nw = ', w) 
    move_robot(v,w)    
#m = min(ranges)

   
    #print(m, ranges.index(m), ranges.index(m)/len(ranges))
    #rospy.loginfo("Received lidar data: %s", data)
def listener():
    rospy.init_node('lidar_listener', anonymous=True)
    #rospy.init_node('move_robot_node', anonymous=True)

    rospy.Subscriber('/velodyne/scan', LaserScan, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()

