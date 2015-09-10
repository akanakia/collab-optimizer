# -*- coding: utf-8 -*-
"""
Created on Sat Sep 05 18:01:21 2015

@author: admin
"""

class RobotData:
    def __init__(self, (x,y), orient, robot_id):
        self.x = x
        self.y = y
        self.orient = orient
        self.robot_id = robot_id