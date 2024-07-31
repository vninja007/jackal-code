#!/usr/bin/env python
from scipy.signal import savgol_filter as sgf, find_peaks as fp

import rospy
import numpy as np
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
    mmWave = [i if i!=float('inf') else 0 for i in data.ranges[rightind:leftind+1][::-1][:300]]

    #assert len(mmWave)==300
    mmWave = sgf(sgf(mmWave,13,5),13,5)
    print('\n'.join(str(i) for i in mmWave))

    peaks = [*fp(mmWave, height=4, distance=60)[0]]
    if np.sign(np.diff(mmWave))[0] < 0 and mmWave[0] > 2:
        peaks = [0] + peaks
    if np.sign(np.diff(mmWave))[-1] > 0 and mmWave[-1] > 2:
        peaks = peaks + [299]
#    print('peaks', [0.401 * (i-150) for i in peaks])

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
    #print('x', x, 'realx', realx)
    print(f'left = {round(data.ranges[leftind],2)}, front = {round(data.ranges[frontind],2)}, right = {round(data.ranges[rightind],2)}')
    print('peaks', peaks)
    #m = min(ranges)


    #print(m, ranges.index(m), ranges.index(m)/len(ranges))
    #rospy.loginfo("Received lidar data: %s", data)
def listener():
    rospy.init_node('lidar_listener', anonymous=True)
    rospy.Subscriber('/velodyne/scan', LaserScan, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()

