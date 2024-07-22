#!/usr/bin/env python3
import rospy
import random
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2, pi

x = 0
y = 0
theta = 0.0
def newOdom(msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

def distance(x1,y1,x2,y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

rospy.init_node("speed_controller")

sub = rospy.Subscriber("/odometry/filtered", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

speed = Twist()
pub.publish(speed)
r = rospy.Rate(4)


def goTo(goalX, goalY):

    goal = Point()
    goal.x = goalX
    goal.y = goalY
    tolerance = .12

    while not rospy.is_shutdown():

        dist = distance(x,y,goal.x,goal.y)
        print(x, y, dist)
        if(dist<tolerance): 
            break
        inc_x = goal.x -x
        inc_y = goal.y -y

        angle_to_goal = atan2(inc_y, inc_x)
        angle_to_goal = angle_to_goal
        angerr = angle_to_goal-theta
        angerr = angerr%(2*pi)
        if(angerr > pi): angerr = angerr-2*pi
        print(angerr)
        if angerr  > 0.07:
            speed.linear.x = 0.0 if angerr > 1 else 0.6*(1-(angerr))
            speed.angular.z = min(angerr,.5)
        elif angerr < -0.07:
            speed.linear.x = 0.0 if angerr < -1 else 0.6 *(1+(angerr))
            speed.angular.z = max(angerr,-.5)
        else:
            speed.linear.x = 0.7
            speed.angular.z = 0.0

        pub.publish(speed)
        r.sleep()    


#for _ in range(5):
#	goTo(random.uniform(-.7,.7), random.uniform(-.7,.7))

goTo(-.7,-.7)
goTo(-.7,.7)
goTo(.7,.7)
goTo(.7,-.7)
goTo(0,0)
