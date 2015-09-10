# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 20:12:46 2015

@author: admin
"""
import math

class RobotSimulator:
    """
    The robot simulator is a very simple class. It's update method takes in a 
    list of RobotData objects and updates their internal attributes based on the
    preset RobotData.curr_action attribute. 
    """
    
    def __init__(self):
        self.sim_time = 0.0
    
    def update(self, robot_data_list, dt, bounds=None):
        """
        The update function simulates dt milliseconds of time per call, i.e. if
        called at a rate of 1000/dt it updates in real time. Provide area bounds
        ((x_min, x_max),(y_min, y_max)) if movement is restricted.
        """
        for rdat in robot_data_list:
            # robot walks forward or backward
            if 'WALK' in rdat.curr_action:
                walk_dir = rdat.orient_rad() # 'FORWARD' is default direction
                if 'BACKWARD' in rdat.curr_action:
                    walk_dir = ((rdat.orient + 180) % 360) * math.pi / 180.
                   
                # move the robot
                rdat.x += (rdat.simonly_lvel * dt / 1000.) * math.cos(walk_dir)
                rdat.y += (rdat.simonly_lvel * dt / 1000.) * math.sin(walk_dir)
                
                # check if movement is within bounds
                if bounds is not None:
                    ((x_min, x_max),(y_min, y_max)) = bounds
                    if rdat.x < x_min:
                        rdat.x = x_min
                    elif rdat.x > x_max:
                        rdat.x = x_max
                    if rdat.y < y_min:
                        rdat.y = y_min
                    elif rdat.y > y_max:
                        rdat.y = y_max
                    
            # robot turns left or right with a narrow or wide angle
            elif 'TURN' in rdat.curr_action:
                if 'LEFT' in rdat.curr_action:
                    rdat.orient += rdat.simonly_rvel * dt / 1000.
                else: # turn 'RIGHT'
                    rdat.orient -= rdat.simonly_rvel * dt / 1000.
                    
                if rdat.orient >= 360:
                    rdat.orient -= 360
                if rdat.orient < 0:
                    rdat.orient += 360
            
            # robot turns on led
            elif rdat.curr_action == 'LED_ON':
                rdat.simonly_color = (0, 0, 200) # Blue
                
            else: # 'NOTHING'
                rdat.simonly_color = (200, 200, 0) # Blue
                
        self.sim_time += dt