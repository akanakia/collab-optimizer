# -*- coding: utf-8 -*-
"""
Created on Sat Sep 05 18:01:21 2015

@author: admin
"""
import random
import math

# *** UNITS ***
# LENGTH/DISTANCE: mm
# TIME: s
# ANGLE: degrees

ROBOT_BASE_LVEL_LOW  = 1.7  # mm/s
ROBOT_BASE_LVEL_HIGH = 5.0  # mm/s
ROBOT_BASE_RVEL_LOW  = 2.75 # deg/s
ROBOT_BASE_RVEL_HIGH = 3.75 # deg/s
ROBOT_RADIUS = 15

class RobotData:
    def __init__(self, (x,y), orient, robot_id, curr_action='NOTHING'):
        self.x = x
        self.y = y
        self.orient = orient
        self.robot_id = robot_id
        self.curr_action = curr_action
        
        # Data for simulator only
        self.simonly_lvel = random.uniform(ROBOT_BASE_LVEL_LOW, ROBOT_BASE_LVEL_HIGH)
        self.simonly_rvel = random.uniform(ROBOT_BASE_RVEL_LOW, ROBOT_BASE_RVEL_HIGH)
        self.simonly_radius = ROBOT_RADIUS
        self.simonly_color = (200, 200, 0) # Yellow
        
    def orient_rad(self):
        return self.orient * math.pi / 180.