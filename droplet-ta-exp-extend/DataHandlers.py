# -*- coding: utf-8 -*-
import random
import math
import taconstants as taconst

# *** UNITS ***
# LENGTH/DISTANCE: mm
# TIME: s
# ANGLE: degrees

ROBOT_BASE_LVEL_LOW  = 1.7  # mm/s
ROBOT_BASE_LVEL_HIGH = 5.0  # mm/s
ROBOT_BASE_RVEL_LOW  = 2.75 # deg/s
ROBOT_BASE_RVEL_HIGH = 3.75 # deg/s

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
        self.simonly_radius = taconst.ROBOT_RADIUS
        self.simonly_color = (200, 200, 0) # Yellow
        
    def orient_rad(self):
        return self.orient * math.pi / 180.

FIRE_INCREASE_INTERVAL_MIN = 3 * 60 # sec
FIRE_INCREASE_INTERVAL_MAX = 4 * 60 # sec
        
class FireData:
    def __init__(self, (x,y), radius, intensity, start_time):
        self.x = x
        self.y = y
        self.radius = radius
        self.intensity = intensity
        
        # This data is stored in ms instead of sec
        self.start_time = start_time
        self.time_alive = 0.
        self._next_fire_inc = 0.
        self.update_fire_inc_interval()
        
    def update_fire_inc_interval(self):
        if self.time_alive >= self._next_fire_inc:        
            self._next_fire_inc = self.time_alive + (random.uniform(FIRE_INCREASE_INTERVAL_MIN, FIRE_INCREASE_INTERVAL_MAX) * 1000)
            return True
    
    def color(self):
        return (200, 8 * self.intensity, 0)
        
        return False
        