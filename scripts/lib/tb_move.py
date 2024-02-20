#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import math

def init():
    #rospy.init_node('move_turtlebot', anonymous=True)

    global rate
    rate = rospy.Rate(10)  # 10 Hz

    # Create a publisher for the Twist messages
    global cmd_vel_pub
    global move_cmd

    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    # Create a Twist message
    move_cmd = Twist()

def stop():
    move_cmd.linear.x = 0.0
    move_cmd.angular.z = 0.0
    cmd_vel_pub.publish(move_cmd)


def move_until_obstacle(distance):

    move_cmd.linear.x = 0.125
    move_cmd.angular.z = 0.0
    
    # 물체(벽)과의 거리가 0.22m일때까지 이동
    # Lidar에서 0.0000m가 나오는 경우도 있으므로 or로 예외처리
    if distance == None:
        return 1

    if distance > 0.21:
        cmd_vel_pub.publish(move_cmd)

        
        return 1
    else:
        stop()
        rospy.loginfo("Moving Done.{}".format(distance))
        return 0


def turn(angle, deg_correction=None, times=None):
    # 각도 보정
    if deg_correction != None:
        if correct_horizontal_theta(deg_correction, times) == 1:
            return 1

    #rospy.loginfo("Turning...")

    # Angular velocity (rad/s)
    angular_speed = 0.5

    move_cmd.linear.x = 0.0

    # 반시계 방향일 경우
    clockwise = angle < 0
    move_cmd.angular.z = angular_speed if clockwise else -angular_speed

    current_angle = 0
    t0 = rospy.Time.now().to_sec()

    while abs(current_angle) < abs(math.radians(angle)):
        cmd_vel_pub.publish(move_cmd)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed * (t1 - t0)
        #rate.sleep()

    stop()
    #rospy.loginfo("Turning Done.")
    return 0


# 물체를 기준으로 각도 보정
def correct_horizontal_theta(deg_correction,times):
    if deg_correction != None:
        rospy.loginfo(deg_correction)

        # 벽의 각도가 0.01도 이상이면
        # -10도와 10도의 거리 측정 결과가 0.1m 미만 일때 보정한다.
        if abs(deg_correction[0]) > 0.0025:
            if  abs(deg_correction[1]) < 0.1:

                turn(deg_correction[0]/times)

                return 1

        else:
            stop()
            return 0
        
    return 1
