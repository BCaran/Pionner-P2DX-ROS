#! /usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
import math

def callback(msg):
    global x
    global y
    global theta
    
    y = msg.pose.pose.position.y
    x = msg.pose.pose.position.x
    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    theta = rad2deg(theta)
    
def goStraightX(goal):
	while 1:
		cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
		move_cmd = Twist()
		if abs(goal - x) > 0.5:
			move_cmd.linear.x = 0.3
		elif (x/goal) < 0.99:
			move_cmd.linear.x = abs(goal - x)*0.5
		else:
			move_cmd.linear.x = 0
			break
		cmd_pub.publish(move_cmd)
		rate = rospy.Rate(10)
		
def goStraightY(goal):
	while 1:
		cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
		move_cmd = Twist()
		if abs(goal - y) > 0.5:
			move_cmd.linear.x = 0.3
		elif (y/goal) < 0.99:
			move_cmd.linear.x = abs(goal - y)*0.5
		else:
			move_cmd.linear.x = 0
			break
		cmd_pub.publish(move_cmd)
		rate = rospy.Rate(10)
		
def goBackX(goal):
	while 1:
		cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
		move_cmd = Twist()
		if abs(goal - x) > 0.5:
			move_cmd.linear.x = 0.3
		elif (1-(x - goal)/1) < 0.99:
			move_cmd.linear.x = abs(goal - x)*0.5
		else:
			move_cmd.linear.x = 0
			break
		cmd_pub.publish(move_cmd)
		rate = rospy.Rate(10)		
		
def goBackY(goal):
	while 1:
		cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
		move_cmd = Twist()
		if abs(goal - y) > 0.5:
			move_cmd.linear.x = 0.3
		elif (1-(x - goal)/1) < 0.99:
			move_cmd.linear.x = abs(goal - y)*0.5
		else:
			move_cmd.linear.x = 0
			break
		cmd_pub.publish(move_cmd)
		rate = rospy.Rate(10)	

def turn(angle_deg):
	while 1:
		cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
		move_cmd = Twist()
		if (theta/angle_deg) > 0.99:
			move_cmd.angular.z = 0.0
			break
		else:
			move_cmd.angular.z = (angle_deg-theta)*0.02
		cmd_pub.publish(move_cmd)
		rate = rospy.Rate(10)

def rad2deg(rad):
	deg = math.degrees(rad)
	if deg < 0:
		deg = deg + 360
	else:		
		deg = deg
	return deg
		
odom_sub = rospy.Subscriber('/odom', Odometry, callback)
rospy.init_node('umb_mark')
rate = rospy.Rate(10) # 10hz


while not rospy.is_shutdown():
	goStraightX(1)
	print(x)
	turn(90)
	print(theta)
	goStraightY(1)
	print(y)
	turn(180)
	print(theta)
	goBackX(0.0)
	print(x)
	turn(270)
	print(theta)
	goBackY(0.0)
	print(y)
	turn(360);
	rate.sleep()
