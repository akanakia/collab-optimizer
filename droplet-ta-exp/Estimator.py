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
        self.rr_screen_width    = rr_screen_width
        self.rr_screen_height   = rr_screen_height        
        
        self.scale_x = float(fire_screen_width)  / rr_screen_width
        self.scale_y = float(fire_screen_height) / rr_screen_height
        
        
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
        action_list = [self.action_set.index('NOTHING') for _ in range(20)]
        
        if len(robot_data) > 0 and len(target_data) > 0:
            for (robot_index, target_index) in self.robot_assignments:
                (robot_x_raw, robot_y_raw, robot_orient, robot_id) = robot_data[robot_index]
                ((target_x, target_y), target_size) = target_data[target_index]
                
                
                # Transform the RoboRealm coordinates to screen coordinates
                robot_x = int(robot_x_raw * self.scale_x)
                robot_y = int((self.rr_screen_height - robot_y_raw) * self.scale_y)
                desired_angle = 0
                print ('Robot (%d,%d) --> Target (%d,%d)'%(robot_x, robot_y, target_x, target_y))  
                
                fire_area = (target_size*self.fire_screen_height*self.fire_screen_width)
                fire_radius = math.sqrt(fire_area/math.pi)           
                robot_pixel_radius = 26
                
                if abs(target_x - robot_x) <= fire_radius-robot_pixel_radius and abs(target_y - robot_y) <= fire_radius-robot_pixel_radius:
                    action_list[self.robot_ids.index(robot_id)] = self.action_set.index('NOTHING')
                    continue
                    
#                elif abs(target_x - robot_x) <= 5:
#                    if target_y < robot_y:
#                        action_list[self.robot_ids.index(robot_id)] = self.action_set.index('WALK_FORWARD')
#                    else:
#                        action_list[self.robot_ids.index(robot_id)] = self.action_set.index('WALK_BACKWARD')
#                    continue
#                
#                elif abs(target_y - robot_y) <= 5:
#                    if target_y < robot_y:
#                        desired_angle = 90
#                    else:
#                        desired_angle = -90
#                        
                delta_y = -(target_y-robot_y)
                delta_x = target_x-robot_x
                desired_angle = math.degrees(math.atan2(delta_y,delta_x))
                desired_angle-=90
                dist = math.sqrt(delta_y*delta_y+delta_x*delta_x)
                    
                angle_threshold = max(math.degrees(abs(math.asin((fire_radius-robot_pixel_radius)/dist))),10)
                
                angle_needed = desired_angle - robot_orient
                
                angle_needed = self.pretty_angle(angle_needed)
                robot_orient = self.pretty_angle(robot_orient)
                desired_angle = self.pretty_angle(desired_angle)
                
                if angle_needed > -angle_threshold and angle_needed < angle_threshold:
                    action_list[self.robot_ids.index(robot_id)] = self.action_set.index('WALK_FORWARD')
                elif angle_needed >= 0 and angle_needed <= 20:
                    action_list[self.robot_ids.index(robot_id)] = self.action_set.index('TURN_LEFT_SHORT')
                elif angle_needed >= 0 and angle_needed <= 180:
                    action_list[self.robot_ids.index(robot_id)] = self.action_set.index('TURN_LEFT_LONG')
                elif angle_needed <= 0 and angle_needed >= -20:
                    action_list[self.robot_ids.index(robot_id)] = self.action_set.index('TURN_RIGHT_SHORT')
                elif angle_needed <= 0 and angle_needed >= -180:
                    action_list[self.robot_ids.index(robot_id)] = self.action_set.index('TURN_RIGHT_LONG')
                print('Current Angle = %f, Desired Angle = %f, Angle to Turn = %f, Angle Threshold = %f'%(robot_orient, desired_angle, angle_needed, angle_threshold))    
                    
        return ''.join([str(a) for a in action_list])
    
    
    def pretty_angle(self, theta):
        return ((theta+180)%360)-180
    