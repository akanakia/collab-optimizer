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
    def __init__(self, (x,y), orient, robot_id, action='NOTHING'):
        self.x = x
        self.y = y
        self.orient = orient
        self.robot_id = robot_id
        self.action = action
        self.target_coords = None
        
        # Data for simulator only
        self.simonly_lvel = random.uniform(ROBOT_BASE_LVEL_LOW, ROBOT_BASE_LVEL_HIGH)
        self.simonly_rvel = random.uniform(ROBOT_BASE_RVEL_LOW, ROBOT_BASE_RVEL_HIGH)
        self.simonly_radius = taconst.ROBOT_RADIUS
        self.simonly_color = (200, 200, 0) # Yellow

FIRE_INCREASE_INTERVAL_MIN = 4 * 60 # sec
FIRE_INCREASE_INTERVAL_MAX = 5 * 60 # sec
        
class FireData:
    def __init__(self, (x,y), radius, intensity, start_time):
        self.x = x
        self.y = y
        self.radius = radius
        self.intensity = intensity
        self.curr_team = []
        
        # This data is stored in ms instead of sec
        self.start_time = start_time
        self.time_alive = 0.
        self._next_fire_inc = 0.
        self._extinguish_timer = 0.
        self.update_fire_inc_interval()

    def update_fire_extinguish_interval(self):
        if len(self.curr_team) >= self.intensity:
            self._extinguish_timer += taconst.SIM_TIMESTEP
            if self._extinguish_timer >= taconst.FIRE_EXTINGUISH_TIME:
                return True
        return False
        
    def update_fire_inc_interval(self):
        if self.time_alive >= self._next_fire_inc:        
            self._next_fire_inc = self.time_alive + (random.uniform(FIRE_INCREASE_INTERVAL_MIN, FIRE_INCREASE_INTERVAL_MAX) * 1000)
            return True
        return False
    
    def color(self):
        return (200, 8 * self.intensity, 0)

class ExpData:
    def set_distance_matrix(self, robot_data_list, fire_data_list):
        """
        Saves a num_robots x num_fires matrix D of distances between robots and
        fire centers.
        """
        self.D = [[math.hypot(fdat.x - rdat.x,fdat.y - rdat.y) for fdat in fire_data_list] for rdat in robot_data_list]
        