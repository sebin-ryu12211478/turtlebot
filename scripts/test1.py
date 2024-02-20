#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

class LaserScanSubscriber:
    def __init__(self):
        #rospy.init_node('laser_scan_subscriber', anonymous=True)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        # Initialize instance variables
        self.distance_at_0_degree = 0.0
        self.distance_at_45_degree = 0.0
        self.distance_at_90_degree = 0.0

    def scan_callback(self, msg):
        # Get angle increment and angle range
        angle_increment = msg.angle_increment
        angle_min = msg.angle_min
        angle_max = msg.angle_max

        # Define the desired angle
        # section in train
        # | 4 | 2 |
        # | 3 | 1 |
        desired_angle_deg = 0
        desired_angle_deg2 = 45  # to identify an object in section 1
        desired_angle_deg3 = 90  # to identify an object in section 3
        desired_angle_rad = math.radians(desired_angle_deg)
        desired_angle_rad2 = math.radians(desired_angle_deg2)
        desired_angle_rad3 = math.radians(desired_angle_deg3)

        # Calculate index corresponding to the desired angle
        index = int((desired_angle_rad - angle_min) / angle_increment)
        index2 = int((desired_angle_rad2 - angle_min) / angle_increment)
        index3 = int((desired_angle_rad3 - angle_min) / angle_increment)

        # Get distance data for the desired angles
        self.distance_at_0_degree = msg.ranges[index]
        self.distance_at_45_degree = msg.ranges[index2]
        self.distance_at_90_degree = msg.ranges[index3]




        self.go_straight_until_clear()

        # Determine if there's an object in the desired direction
       # if self.distance_at_0_degree < 0.1:  # If less than 10cm away
            
           # self.stop_robot()
            
        self.turn_robot(math.radians(90))

            # Go straight until section 4 
        #self.go_straight_until_obstacle(6.0) # duration seconds.
        

            # if section 1 is empty, go to the section 1. 
        if self.distance_at_45_degree > 0.2:  # when there's no robot in section 1
                self.go_straight_until_clear()
                self.turn_robot(math.radians(90))
                self.go_straight_until_clear()
                self.turn_robot(math.radians(180)) # now the robot is in section 1. 
        else: # if there's a robot in section 1, check whether section 2 is empty or not.
                if self.distance_at_0_degree > 0.2:  # when there is no robot in 2, go to section 2.
                    self.go_straight_until_clear()
                    self.turn_robot(math.radians(180)) # now the robot is in section 2. 
                else: # when there are robots in section 1 and 2, check if 3 is empty or not.
                    if self.distance_at_90_degree > 0.2: # if the section 3 is empty.
                        self.turn_robot(math.radians(90))
                        self.go_straight_until_clear()
                        self.turn_robot(math.radians(180)) # now the robot is in section 3.
                    elif self.distance_at_90_degree < 0.2:
                        self.turn_robot(math.radians(180))
                
     #   else:
            # Go straight until an obstacle is detected
     #       self.go_straight_until_obstacle()



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

    def go_straight_until_obstacle(self):
        move_cmd.linear.x = 0.1  # Linear velocity (m/s)
        move_cmd.angular.z = 0.0
        cmd_vel_pub.publish(move_cmd)

    # to go straight until section 4 
    def go_straight_until_obstacle(self, duration): 
        move_cmd.linear.x = 0.1  # Linear velocity (m/s)
        move_cmd.angular.z = 0.0
        cmd_vel_pub.publish(move_cmd)
        start_time = rospy.Time.now()  # Define start time
        while (rospy.Time.now() - start_time).to_sec() < duration:
            pass
        self.stop_robot()
   

    def go_straight_until_clear(self):
        move_cmd.linear.x = 0.1  # Linear velocity (m/s)
        move_cmd.angular.z = 0.0
        if self.distance_at_0_degree < 0.1:
            cmd_vel_pub.publish(move_cmd)

        # Keep moving until no obstacle in front
        while not rospy.is_shutdown():
            if self.distance_at_0_degree < 0.15:  # If more than 15cm away
                self.stop_robot()
                break

if __name__ == '__main__':
    try:
        # Initialize node
        rospy.init_node(['laser_scan_subscriber', 'move_turtlebot'], anonymous=True)

        # Create a publisher for the Twist messages
        cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # Create a Twist message
        move_cmd = Twist()
        move_cmd.linear.x = 0.0  # Linear velocity (m/s)
        move_cmd.angular.z = 0.0  # Angular velocity (rad/s)

        # Initialize LaserScanSubscriber
        laser_subscriber = LaserScanSubscriber()

        # Spin until shutdown
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
