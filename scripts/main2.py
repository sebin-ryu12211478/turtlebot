#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

from lib import tb_move
from lib import ros_lidar as ld

import numpy as np
import math


if __name__ == '__main__':

    try:
        rospy.init_node(['move_turtlebot', 'laser_scan_subscriber'], anonymous=True)

        tb_move.init()
        tb_move.stop()

        # Initialize LaserScanSubscriber
        lidar = ld.LaserScanSubscriber()

        # Wait for the subscriber to initialize
        rospy.sleep(1)  
        
        state = 0

        while 1:

            while tb_move.move_until_obstacle(ld.get_distance(lidar,0)):
                continue
            print(ld.get_distance(lidar, -10),ld.get_distance(lidar, 10))
            rospy.loginfo(ld.get_errdata(lidar))
            input("C")
            times = 1
            while tb_move.turn(180, ld.get_errdata(lidar), times):
                times = times + 20
                continue

        # Spin until shutdown
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
