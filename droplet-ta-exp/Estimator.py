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
        
        self.robot_assignments = None
        
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
            if size <= .005:
                team_sizes.append(((x, y), 0))
            elif size >= .25:
                team_sizes.append((x,y), 20)
            else:
                team_sizes.append(((x,y), int(4.6012 * math.log(308.89 * size))))
                
        return team_sizes
        
    def get_required_team_sizes(self, target_data):
        team_sizes = []
        for ((x,y),size) in target_data:
            if size <= .005:
                team_sizes.append(0)
            elif size >= .25:
                team_sizes.append(20)
            else:
                team_sizes.append(int(4.6012 * math.log(308.89 * size)))
          
        return team_sizes
        
    def estimate_robot_constraints(self, target_data, robot_data):
        """
        Estimates the constraint set of targets for each robot. I'm leaving this
        empty for now.
        """
        return []
        
    def set_current_assignments(self, M):
        """
        This function MUST be called before calling computer_robot_action_list().
        Used to update the current list of robot-object assignments.
        """
        self.robot_assignments = [(robot_index, target_row.index(1)) for (robot_index, target_row) in enumerate(M) if 1 in target_row]
        self.robots_at_target = {}
        for (robot_index, target_index) in self.robot_assignments:
            self.robots_at_target[target_index] = []
        
    def compute_robot_action_list(self, target_data, robot_data):
        """
        Creates the action list to send to the serial controller to communicate
        actions to robots if the SMT solver has assignments ready for them. If
        the self.robot_assignments variable is not set then the robots are told
        to do nothing and wait for further assignments.
        Use the set_current_assignments() function to set the robot assignment
        matrix.
        """           
        action_list = [self.action_set.index('NOTHING') for _ in range(20)]
        required_sizes = self.get_required_team_sizes(target_data)
        if self.robot_assignments is None:
            return ''.join([str(_) for _ in action_list])
    
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
                    #We're in the fire; hurray!
                    action_list[self.robot_ids.index(robot_id)] = self.action_set.index('NOTHING')
                    self.robots_at_target[target_index].append(robot_index)
                    continue
                                           
                delta_y = -(target_y-robot_y)
                delta_x = target_x-robot_x
                desired_angle = math.degrees(math.atan2(delta_y,delta_x)) - 90
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
          
        completed_targets = set([])          
        for (robot_index, target_index) in self.robot_assignments:          
            if len(self.robots_at_target[target_index])>=required_sizes[target_index]:
                action_list[self.robot_ids.index(robot_id)] = self.action_set.index('LED_ON')
                completed_targets.add(target_data[target_index][0])
        
        
        self.robot_assignments = None          
        return (''.join([str(a) for a in action_list]), completed_targets)
    
    
    def pretty_angle(self, theta):
        return ((theta+180)%360)-180
    