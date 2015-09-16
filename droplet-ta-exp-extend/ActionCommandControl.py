# -*- coding: utf-8 -*-
import math

class ActionCommandControl:
    def __init__(self):
        pass
        
    def generate_robot_actions(self, robot_data_list, fire_data_list):        
        # Check if any robots are already at a fire
        for rdat in robot_data_list:
            if rdat.target_coords is not None:
                (fx, fy) = rdat.target_coords
                for fdat in fire_data_list:
                    if fdat.x == fx and fdat.y == fy and math.hypot(rdat.x-fdat.x,rdat.y-fdat.y) <= fdat.radius:
                        rdat.target_coords = None                        
                        rdat.action = 'NOTHING'
                        fdat.curr_team.append(rdat.id)                        
                        
        # Check if any fires are ready to act on
        for fdat in fire_data_list:
            if len(fdat.curr_team) == fdat.intensity:
                for rdat in robot_data_list:
                    if rdat.id in fdat.curr_team:
                        rdat.action = 'LED_ON'
                        
        # Move the robots that need moving
        for rdat in robot_data_list:
            if rdat.target_coords is not None:
                (fx, fy) = rdat.target_coords
                angle_needed = self._pretty_angle(math.degrees(math.atan2(rdat.y-fy,rdat.x-fx)) - rdat.orient)
                
                angle_threshold = 15 # degrees
#                angle_threshold = max(math.degrees(abs(math.asin((fire_radius-robot_pixel_radius)/dist))),10)
                if angle_needed >= -angle_threshold and angle_needed <= angle_threshold:
                    rdat.action = 'MOVE_FORWARD'
                elif angle_needed < -angle_threshold:
                    rdat.action = 'TURN_RIGHT'
                else: # angle_needed > angle_threhold
                    rdat.action = 'TURN_LEFT'
                
    def _pretty_angle(self, theta):
        return ((theta+180)%360)-180