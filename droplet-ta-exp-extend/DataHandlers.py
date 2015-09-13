# -*- coding: utf-8 -*-
import random
import math
import taconstants as taconst

# *** UNITS ***
# LENGTH/DISTANCE: mm
# TIME: s
# ANGLE: degrees

class RobotData:
    def __init__(self, (x,y), orient, robot_id, curr_action='NOTHING'):
        self.x = x
        self.y = y
        self.orient = orient
        self.robot_id = robot_id
        self.curr_action = curr_action
        
        # Data for simulator only
        self.simonly_lvel = random.uniform(taconst.ROBOT_BASE_LVEL_LOW, taconst.ROBOT_BASE_LVEL_HIGH)
        self.simonly_rvel = random.uniform(taconst.ROBOT_BASE_RVEL_LOW, taconst.ROBOT_BASE_RVEL_HIGH)
        self.simonly_radius = taconst.ROBOT_RADIUS
        self.simonly_color = (200, 200, 0) # Yellow
        
    def orient_rad(self):
        return self.orient * math.pi / 180.
        
class FireData:
    def __init__(self, x, y, radius, intensity):
        self.x = x
        self.y = y
        self.radius = radius
        self.intensity