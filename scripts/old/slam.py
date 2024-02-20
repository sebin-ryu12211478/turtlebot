#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

import math

def move_turtlebot():
    rospy.init_node('move_turtlebot', anonymous=True)
    rate = rospy.Rate(10)  # 10 Hz

    # Create a publisher for the Twist messages
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    # Create a Twist message
    move_cmd = Twist()
    move_cmd.linear.x = 0.01  # Linear velocity (m/s)
    move_cmd.angular.z = 0.0  # Angular velocity (rad/s)
#
    while not rospy.is_shutdown():
        cmd_vel_pub.publish(move_cmd)
        rate.sleep()

class LaserScanSubscriber:
    def __init__(self):
        rospy.init_node('laser_scan_subscriber', anonymous=True)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)

    def scan_callback(self, msg):
        # Get angle increment and angle range
        angle_increment = msg.angle_increment
        angle_min = msg.angle_min
        angle_max = msg.angle_max

        # Define the desired angle
        desired_angle_deg = 0  
        desired_angle_rad = math.radians(desired_angle_deg)

        # Calculate index corresponding to the desired angle
        index = int((desired_angle_rad - angle_min) / angle_increment)

        # Get distance data for the desired angle
        distance_at_desired_angle = msg.ranges[index]

        # Print the distance
        rospy.loginfo("Distance at {} degrees: {:.2f} meters".format(desired_angle_deg, distance_at_desired_angle))

if __name__ == '__main__':
    try:
        laser_scan_subscriber = LaserScanSubscriber()
        move_turtlebot()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
