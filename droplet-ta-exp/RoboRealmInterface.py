# -*- coding: utf-8 -*-
from RR_API import *

class RoboRealmInterface:
    def __init__(self):
        self.rr = RR_API()

    def connect(self):
        self.rr.Connect('localhost')
        
    def get_robot_positions(self):
        """
        Returns a 3-tuple list containing the robot's pixel row, column, 
        and orientation
        """
        robots_col = ''
        robots_row = ''
        robots_orient = ''
        
        robots_col = map(int, map(float, [cols.strip() for cols in self.rr.GetVariable('FIDUCIAL_X_COORD_ARRAY').split(',')]))
        robots_row = map(int, map(float, [rows.strip() for rows in self.rr.GetVariable('FIDUCIAL_Y_COORD_ARRAY').split(',')]))
        robots_orient = map(float, [orients.strip() for orients in self.rr.GetVariable('FIDUCIAL_ORIENTATION_ARRAY').split(',')])
            
        return zip(robots_row, robots_col, robots_orient)