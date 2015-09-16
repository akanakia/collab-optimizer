# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 20:12:46 2015

@author: admin
"""
import math
import random

from DataHandlers import RobotData
import taconstants as taconst

class RobotSimulator:
    """
    The robot simulator is a very simple class. It's update method takes in a 
    list of RobotData objects and updates their internal attributes based on the
    preset RobotData.action attribute. 
    """
    
    def __init__(self):
        self.sim_time = 0.
    
    def init(self, num_robots, bounds):
        """
        Returns a randomly generated RobotData object list of size num_robots. 
        Arena bounds are specified as ((x_min, x_max), (y_min, y_max)) in mm.
        """
        ((x_min, x_max),(y_min, y_max)) = bounds
        return [RobotData((random.randint(x_min + taconst.ROBOT_RADIUS, x_max - taconst.ROBOT_RADIUS), random.randint(y_min + taconst.ROBOT_RADIUS, y_max - taconst.ROBOT_RADIUS)), (30 * i)%360, i, 'WALK_FORWARD') for i in range(num_robots)]
    
    def update(self, robot_data_list, bounds=None):
        """
        The update function simulates taconst.SIM_TIMESTEP milliseconds of time per call, i.e. if
        called at a rate of 1000/taconst.SIM_TIMESTEP it updates in real time. Provide arena bounds
        ((x_min, x_max),(y_min, y_max)) in mm if movement is restricted.
        """
        for rdat in robot_data_list:
            # robot walks forward or backward
            if 'WALK' in rdat.action:
                walk_dir = math.radians(rdat.orient) # 'FORWARD' is default direction
                if 'BACKWARD' in rdat.action:
                    walk_dir = ((rdat.orient + 180) % 360) * math.pi / 180.
                   
                # move the robot
                rdat.x += (rdat.simonly_lvel * taconst.SIM_TIMESTEP / 1000.) * math.cos(walk_dir)
                rdat.y += (rdat.simonly_lvel * taconst.SIM_TIMESTEP / 1000.) * math.sin(walk_dir)
                
                # check if movement is within bounds
                if bounds is not None:
                    ((x_min, x_max),(y_min, y_max)) = bounds
                    rdat.x = max(x_min + taconst.ROBOT_RADIUS, min(x_max - taconst.ROBOT_RADIUS, rdat.x))
                    rdat.y = max(y_min + taconst.ROBOT_RADIUS, min(y_max - taconst.ROBOT_RADIUS, rdat.y))
                    
            # robot turns left or right with a narrow or wide angle
            elif 'TURN' in rdat.action:
                if 'LEFT' in rdat.action:
                    rdat.orient += rdat.simonly_rvel * taconst.SIM_TIMESTEP / 1000.
                else: # turn 'RIGHT'
                    rdat.orient -= rdat.simonly_rvel * taconst.SIM_TIMESTEP / 1000.
                    
                if rdat.orient >= 360:
                    rdat.orient -= 360
                if rdat.orient < 0:
                    rdat.orient += 360
            
            # robot turns on led
            elif rdat.action == 'LED_ON':
                rdat.simonly_color = (0, 0, 200) # Blue
                
            else: # 'NOTHING'
                rdat.simonly_color = (200, 200, 0) # Yellow
                
        self.sim_time += taconst.SIM_TIMESTEP