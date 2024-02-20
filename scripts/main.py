#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

import math
import getmac

from lib import tb_move
from lib import ros_lidar as ld
from lib import socket_teleop



if __name__ == '__main__':

    try:
        rospy.init_node(['move_turtlebot', 'laser_scan_subscriber'], anonymous=True)

        tb_move.init()
        tb_move.stop()

        #client_sc = socket_teleop.Socket_Teleop()

        # Initialize LaserScanSubscriber
        lidar = ld.LaserScanSubscriber()

        # Wait for the subscriber to initialize
        rospy.sleep(1)  
        
        
        input("PRESS ENTER : ")
        sum = 0
        for i in range(0,10):
            tmp = lidar.correct_bias()
            sum += tmp
            rospy.sleep(0.1)  
        lidar.bias = sum/10
        input("PRESS ENTER : ")
        
        state = 1
        while 1:

            #state = client_sc.receive()
            #client_sc.debug_mode()

            if state == 1:
                for deg in [90,90,180]:
                    avg = lidar.get_distance(0)
                    while tb_move.move_until_obstacle(avg):
                        avg = lidar.get_distance(0)
                        continue

                    times = 1
                    while tb_move.turn(deg, lidar.get_errdata(), times):
                        times = times + 20
                        continue

                state = 2

                #client_sc.send_all(98)

            if state == 2:
                for deg in [-90,-90,180]:
                    while tb_move.move_until_obstacle(lidar.get_distance(0)):
                        continue

                    times = 1
                    while tb_move.turn(deg, lidar.get_errdata(), times):
                        times = times + 20
                        continue

                #client_sc.send_all(99)
                #client_sc.close()
                state = 0
                break
                    

        # Spin until shutdown
        #rospy.spin()

    except rospy.ROSInterruptException:
        pass
