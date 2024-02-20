#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math
from lib import tb_move

class LaserScanSubscriber:
    def __init__(self):
        #rospy.init_node('laser_scan_subscriber', anonymous=True)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        # Initialize instance variables
        self.distance = [0.0, 0.0, 0.0]

    def scan_callback(self, msg):
        # Get angle increment and angle range
        angle_increment = msg.angle_increment
        angle_min = msg.angle_min
        angle_max = msg.angle_max

        # Define the desired angle
        # section in train
        # | 4 | 2 |
        # | 3 | 1 |

        desired_angle_deg = [0,45,90]
        desired_angle_rad = [0,0,0]
        index = [0,0,0]

        for i in range(0,3):
            #desired_angle_rad[i] = math.radians(desired_angle_deg[i])
            # rotate lidar
            desired_angle_rad[i] = math.radians((desired_angle_deg[i]+180)%360)

            # Calculate index corresponding to the desired angle
            index[i] = int((desired_angle_rad[i] - angle_min) / angle_increment)

            # Get distance data for the desired angles
            self.distance[i] = msg.ranges[index[i]]

        # ======
        tb_move.go_straight_until_obstacle(self.distance[0])

if __name__ == '__main__':

    try:
        rospy.init_node(['move_turtlebot', 'laser_scan_subscriber'], anonymous=True)

        tb_move.init()
        tb_move.stop()

        # Initialize LaserScanSubscriber
        lidar = LaserScanSubscriber()

        # Spin until shutdown
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
