# -*- coding: utf-8 -*-
class Estimator:
    """
    This class estimates the team size requirements for targets based on their
    relative sizes.
    It also estimates constraint sets for robots based on their relative
    distances to targets.
    """
    def __init__(self, fire_screen_width, fire_screen_height, rr_screen_width, rr_screen_height):
        self.scale_x = fire_screen_width / rr_screen_width
        self.scale_y = fire_screen_height / rr_screen_height
        
        # define closeness tolerances
        self.tol_x = 50
        self.tol_y = 50
        self.robot_ids = ['2B4E', '7D78', '8B46', 'C806', '4177', '0A0B', '3B49', '028C', '1F08', 'EEB0', 'A649', 'A5B5', 'F60A', 'B944', '3405', '43BA', '6648', '1B4B', 'C24B', '4DB0']
        
    def estimate_required_team_sizes(fire_data):
        pass
    
    def estimate_robot_constraints(fire_data, robot_data):
        pass
        
    def compute_robot_action_list(fire_data, robot_data, M):
        pass