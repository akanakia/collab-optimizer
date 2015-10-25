# -*- coding: utf-8 -*-
import math

import taconstants as taconst

class ActionCommandControl:        
    def generate_robot_actions(self, robot_data_list, fire_data_list):
        # check if any robots are at an extinguished fire
        for rdat in robot_data_list:
            if rdat.action == 'LED_ON':
                self._remove_completed_robot_target(rdat, fire_data_list)
        
        # Check if any robots have reached a fire
        for rdat in robot_data_list:
            if rdat.action != 'WAITING' and rdat.action != 'LED_ON' and rdat.target_coords is not None:
                (fx, fy) = rdat.target_coords
                for fdat in fire_data_list:
                    if fdat.x == fx and fdat.y == fy and math.hypot(rdat.x-fdat.x,rdat.y-fdat.y) <= fdat.radius:
                        rdat.action = 'WAITING'
                        fdat.curr_team.append(rdat.robot_id)                        
                        
        # Check if any fires are ready to act on
        for fdat in fire_data_list:
            if len(fdat.curr_team) == fdat.intensity:
                for rdat in robot_data_list:
                    if rdat.robot_id in fdat.curr_team:
                        rdat.action = 'LED_ON'
        
        # Check if any robots have old fire targets and remove them
        for rdat in robot_data_list:
            self._remove_completed_robot_target(rdat, fire_data_list)
                
        # Move the robots that need moving
        for rdat in robot_data_list:
            if rdat.target_coords is not None and rdat.action != 'WAITING' and rdat.action != 'LED_ON':
                (fx, fy) = rdat.target_coords
                angle_needed = self._pretty_angle(math.degrees(math.atan2(fy-rdat.y,fx-rdat.x))  - rdat.orient)
                angle_threshold = 10 # degrees
                for fdat in fire_data_list:
                    if fdat.x == fx and fdat.y == fy:
                        asin_domain_constrained = min(1, max((fdat.radius-taconst.ROBOT_RADIUS)/math.hypot(fdat.y-rdat.y,fdat.x-rdat.x), -1))
                        angle_threshold = self._pretty_angle(max(math.degrees(abs(math.asin(asin_domain_constrained))), angle_threshold))
                        break

                if angle_needed >= -angle_threshold and angle_needed <= angle_threshold:
                    rdat.action = 'WALK_FORWARD'
                elif angle_needed < -angle_threshold:
                    rdat.action = 'TURN_RIGHT'
                else: # angle_needed > angle_threhold
                    rdat.action = 'TURN_LEFT'
                
    def _pretty_angle(self, theta):
        return ((theta+180)%360)-180
        
    def _remove_completed_robot_target(self, robot_data, fire_data_list):
        if robot_data.target_coords is not None:
            (fx, fy) = robot_data.target_coords
            target_found = False
            for fdat in fire_data_list:
                if fdat.x == fx and fdat.y == fy:
                    target_found = True
                    break
            if not target_found:
                robot_data.action = 'NOTHING'
                robot_data.target_coords = None
            return True
        else:
            return False
            