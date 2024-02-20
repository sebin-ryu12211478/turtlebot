#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math
import cv2
from ultralytics import YOLO

def stop_robot(self):
        move_cmd.linear.x = 0.0
        move_cmd.angular.z = 0.0
        cmd_vel_pub.publish(move_cmd)

def turn_robot(self, angle):
        # Assume clockwise rotation for simplicity
        move_cmd.linear.x = 0.0
        move_cmd.angular.z = 0.5  # Angular velocity (rad/s)
        cmd_vel_pub.publish(move_cmd)
        rospy.sleep(angle / 0.5)  # Sleep duration calculated based on desired angle and angular velocity
        self.stop_robot()


def move_turtlebot():
    rospy.init_node('move_turtlebot', anonymous=True)
    rate = rospy.Rate(10)  # 10 Hz

    # Create a publisher for the Twist messages
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    # Create a Twist message
    move_cmd = Twist()
    move_cmd.linear.x = 0.0  # Linear velocity (m/s)
    move_cmd.angular.z = 0.0  # Angular velocity (rad/s)
#
    while not rospy.is_shutdown():
        cmd_vel_pub.publish(move_cmd)
        rate.sleep()

if __name__ == '__main__':
    try:
        cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        move_cmd = Twist()
        move_cmd.linear.x = 0.0  # Linear velocity (m/s)
        move_cmd.angular.z = 0.0  # Angular velocity (rad/s)

        move_turtlebot()
        turn_robot(math.radians(90))

    except rospy.ROSInterruptException:
        pass
