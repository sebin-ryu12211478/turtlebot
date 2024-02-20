#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
import math
import numpy as np

class LaserScanSubscriber:
    def __init__(self):
        #rospy.init_node('laser_scan_subscriber', anonymous=True)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        global PRESET_ANGLE
        global PRESET_ANGLE_LEN

        self.bias = 0

        PRESET_ANGLE = [-10, -5, 0, 5, 10, 90, 180, 270]
        PRESET_ANGLE_LEN = len(PRESET_ANGLE)

        self.distance = np.zeros(PRESET_ANGLE_LEN, dtype=np.float32)


    def scan_callback(self, msg):
        # Get angle increment and angle range
        angle_increment = msg.angle_increment
        angle_min = msg.angle_min
        angle_max = msg.angle_max

        desired_angle_deg = PRESET_ANGLE
        desired_angle_rad = np.zeros(PRESET_ANGLE_LEN)
        index = np.zeros(PRESET_ANGLE_LEN, dtype=int)

        for i in range(0,PRESET_ANGLE_LEN):
            distance_raw = np.zeros(5)

            # rotate lidar
            #desired_angle_rad[i] = math.radians(desired_angle_deg[i])
            desired_angle_rad[i] = math.radians((desired_angle_deg[i]+180)%360)

            # Calculate index corresponding to the desired angle
            index[i] = int((desired_angle_rad[i] - angle_min) / angle_increment)

            # Get distance data for the desired angles
            self.distance[i] = round(msg.ranges[index[i]],3)


        # Print the distance

    def get_distance_ori(self):
        return self.distance

    def get_distance(self, deg=None):
        distance = self.get_distance_ori()
        for i in distance:
            if round(i,3) == 0.000 or i < 0.00001:
                return None

            if deg == None:
                return distance

            return distance[self.get_index(deg)]

        return None



    def get_position(self, deg, length=None):
        rad = np.radians(deg)
        if length != None:
            return (length*np.cos(rad), length*np.sin(rad))


    def get_errdata(self):
        if self.get_distance(0) > 0.5:
            return None


        distance_L = self.get_distance(-10)
        distance_R = self.get_distance(10) + self.bias
        # +0.01 : 라이다 자체의 오차

        XL, YL =  self.get_position(-10, distance_L)
        XR, YR =  self.get_position(10, distance_R)

        theta = np.degrees(np.arctan((XR-XL)/(YR-YL)))
        diff = abs(distance_L-distance_R)
        return [theta, diff]


    def correct_bias(self):

        distance_L = self.get_distance(-10)
        distance_R = self.get_distance(10)
        # +0.01 : 라이다 자체의 오차

        BIAS = distance_L-distance_R

        return BIAS

    def get_index(self, deg):
        return PRESET_ANGLE.index(deg)