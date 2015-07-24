# -*- coding: utf-8 -*-
import math

class Estimator:
    """
    This class estimates the team size requirements for targets based on their
    relative sizes.
    It also estimates constraint sets for robots based on their relative
    distances to targets.
    """
    def __init__(self, fire_screen_width, fire_screen_height, rr_screen_width, rr_screen_height):
    
        self.fire_screen_width  = fire_screen_width
        self.fire_screen_height = fire_screen_height
        self.rr_scrren_width    = rr_screen_width
        self.rr_scrren_height   = rr_screen_height        
        
        self.scale_x = fire_screen_width  / rr_screen_width
        self.scale_y = fire_screen_height / rr_screen_height
        
        
        # define closeness tolerances
        self.tol_x = 50
        self.tol_y = 50
        
        # define droplet id to index mapping and action set mapping
        self.robot_ids = ['2B4E', '7D78', '8B46', 'C806', '4177', '0A0B', '3B49', '028C', '1F08', 'EEB0', 'A649', 'A5B5', 'F60A', 'B944', '3405', '43BA', '6648', '1B4B', 'C24B', '4DB0']
        self.action_set = ['NOTHING', 'WALK_FORWARD', 'WALK_BACKWARD', 'TURN_LEFT_SHORT', 'TURN_RIGHT_SHORT', 'TURN_LEFT_LONG', 'TURN_RIGHT_LONG', 'LED_ON']
        
    def estimate_required_team_sizes(self, target_data):
        """
        Given the relative size of the target this function returns a 2-tuple of 
        the form ((x, y), team-size) where (x,y) is the center of the target and
        its unique identifier and team-size is the estimated team size of robots
        required to complete it.
        To understand the math contants in this function look at Mathematica
        Notebook data/TeamSizeEstimation.nb in this repository
        """
        team_sizes = []
        for ((x, y), size) in target_data:
            # We don't assign any robots to target until they are large enough
            # to cover at least 1% of the total screen area
            if size <= .1:
                team_sizes.append(((x, y), 0))
            else:
                team_sizes.append(((x,y), int(8.65617 * math.log(12.5992 * size))))
                
        return team_sizes
        
    def estimate_robot_constraints(self, target_data, robot_data):
        """
        Estimates the constraint set of targets for each robot. I'm leaving this
        empty for now.
        """
        pass
        
    def set_current_assignments(self, M):
        """
        This function MUST be called before calling computer_robot_action_list().
        Used to update the current list of robot-object assignments.
        """
        self.robot_assignments = [(robot_index, target_row.index(1)) for (robot_index, target_row) in enumerate(M) if 1 in target_row]
        
    def compute_robot_action_list(self, target_data, robot_data):
        """
        Creates the action list to send to the serial controller to communicate
        actions to robots        
        """
        action_list = [self.action_set.index('NOTHING') for _ in len(self.robot_ids)]
            
        for (robot_index, target_index) in self.robot_assignments:
            (robot_x_raw, robot_y_raw, robot_orient, robot_id) = robot_data[robot_index]
            ((target_x, target_y), target_size) = target_data[target_index]
            
            # Transform the RoboRealm coordinates to screen coordinates
            robot_x = robot_x_raw * self.scale_x
            robot_y = (self.rr_scrren_height - robot_y_raw) * self.scale_y
            desired_angle = 0
            
            if abs(target_x - robot_x) <= 50 and abs(target_y - robot_y) <= 50:
                action_list[self.robot_ids.index(robot_id)] = self.action_set.index('NOTHING')
                continue
                
            elif abs(target_x - robot_x) <= 5:
                if target_y < robot_y:
                    action_list[self.robot_ids.index(robot_id)] = self.action_set.index('WALK_FORWARD')
                else:
                    action_list[self.robot_ids.index(robot_id)] = self.action_set.index('WALK_BACKWARD')
                continue
            
            elif abs(target_y - robot_y) <= 5:
                if target_y < robot_y:
                    desired_angle = 90
                else:
                    desired_angle = -90
                    
            else:
                robot_y = -robot_y
                target_y = -target_y
                desired_angle = math.atan(float(target_y - robot_y)/(target_x - robot_x))
            
            angle_needed = desired_angle - robot_orient
            if angle_needed > 180:
                angle_needed = 360 - angle_needed
            if angle_needed < -180:
                angle_needed = 360 + angle_needed
            
            if angle_needed > -5 and angle_needed < 5:
                action_list[self.robot_ids.index(robot_id)] = self.action_set.index('WALK_FORWARD')
            elif angle_needed >= 0 and angle_needed <= 20:
                action_list[self.robot_ids.index(robot_id)] = self.action_set.index('TURN_LEFT_SHORT')
            elif angle_needed >= 0 and angle_needed <= 180:
                action_list[self.robot_ids.index(robot_id)] = self.action_set.index('TURN_LEFT_LONG')
            elif angle_needed <= 0 and angle_needed >= -20:
                action_list[self.robot_ids.index(robot_id)] = self.action_set.index('TURN_RIGHT_SHORT')
            elif angle_needed <= 0 and angle_needed >= -180:
                action_list[self.robot_ids.index(robot_id)] = self.action_set.index('TURN_RIGHT_LONG')
                
        return ''.join(action_list)
        