# -*- coding: utf-8 -*-
from RR_API import RR_API

class RoboRealmInterface:
    def __init__(self, rr_x=1000, rr_y=1000):
        self.rr = RR_API()
        self.rr_x = rr_x
        self.rr_y = rr_y

    def connect(self):
        self.rr.Connect('localhost')
        
    def get_robot_positions(self):
        """
        Returns a 4-tuple list containing the robot's (x, y, orientation, id).
        """
        robots_id = [id.strip()[1:5] for id in self.rr.GetVariable('FIDUCIAL_NAME_ARRAY').split(',')]
        robots_x = map(int, map(float, [x.strip() for x in self.rr.GetVariable('FIDUCIAL_X_COORD_ARRAY').split(',')]))
        robots_y = map(int, map(float, [y.strip() for y in self.rr.GetVariable('FIDUCIAL_Y_COORD_ARRAY').split(',')]))
        robots_orient = map(float, [orient.strip() for orient in self.rr.GetVariable('FIDUCIAL_ORIENTATION_ARRAY').split(',')])
            
        return zip(robots_x, robots_y, robots_orient, robots_id)