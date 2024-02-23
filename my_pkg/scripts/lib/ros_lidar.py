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

        self.difference_LR_distance = 0

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


    def get_distance(self, deg=None):
        distance = self.distance
        
        if deg == None:
            for i in distance:
                # 라이다에서 거리가 0.0m 으로 나오는 경우 무시
                if i < 0.00001:
                    return None
            return distance
        else:
            if distance[self.get_degree_index(deg)] < 0.00001:
                return None

            return distance[self.get_degree_index(deg)]


    # 극 좌표 -> 직교 좌표
    def get_position(self, length, deg):
        rad = np.radians(deg)
        if length != None:
            return (length*np.cos(rad), length*np.sin(rad))


    # 정면의 벽과 이루는 각도 산출
    def get_horizontal_theta(self):
        if self.get_distance(0) == None or self.get_distance(-10) == None or self.get_distance(10) == None:
            return None
        if self.get_distance(0) > 0.5:
            return None


        distance_L = self.get_distance(-10)
        distance_R = self.get_distance(10) + self.difference_LR_distance
        # + self.difference_LR_distance : 라이다 자체의 오차

        XL, YL =  self.get_position(distance_L, -10)
        XR, YR =  self.get_position(distance_R, 10)

        theta = np.degrees(np.arctan((XR-XL)/(YR-YL)))
        diff = abs(distance_L-distance_R)
        return [theta, diff]


    # 라이다 좌우(-10, 10)의 오차 산출
    def get_difference_LR_distance(self):

        distance_L = self.get_distance(-10)
        distance_R = self.get_distance(10)

        diff = distance_L-distance_R
        return diff

    def get_degree_index(self, deg):
        return PRESET_ANGLE.index(deg)