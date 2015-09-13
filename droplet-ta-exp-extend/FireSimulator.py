# -*- coding: utf-8 -*-
import taconstants as taconst
from DataHandlers import FireData
import math
import random

MIN_NEW_FIRE_INTENSITY = 2
MAX_NEW_FIRE_INTENSITY = 5
MAX_RANDOM_LOCATION_ATTEMPTS = 200

class FireSimulator:
    def __init__(self):
        self._sim_time = 0.
        
    def init(self):
        pass

    def start_fire(self, fire_data_list, bounds=None, loc=None):
        """
        """
        new_fire_intensity = random.randint(MIN_NEW_FIRE_INTENSITY, MAX_NEW_FIRE_INTENSITY)
        new_fire_radius = taconst.ROBOT_RADIUS / math.sin(math.pi / new_fire_intensity)
        
        if loc is None:
            # Add fire to an available random location
            if bounds is not None:
                ((x_min, x_max), (y_min, y_max)) = bounds
            else:
                print('bounds must be specified for random fire generation')
                return
            
            for attempt in range(MAX_RANDOM_LOCATION_ATTEMPTS):
                (x, y) = (random.randint(x_min, x_max), random.randint(y_min, y_max))
                good_point_found = True
                for fdat in fire_data_list:
                    if math.hypot(fdat.x - x, fdat.y - y) <= fdat.radius:
                        good_point_found = False
                        break
                if good_point_found:
                    break
            
            fire_data_list.append(FireData((x,y), new_fire_radius, new_fire_intensity, self._sim_time))
                    
        else:
            fire_data_list.append(FireData(loc, new_fire_radius, new_fire_intensity, self._sim_time))
    
    def stop_fire(self, fire_data_list, loc):
        """
        """
        (loc_x, loc_y) = loc
        found_fire = None
        for fdat in fire_data_list:
            if fdat.x == loc_x and fdat.y == loc_y:
                found_fire = fdat
                break
        if found_fire is not None:
            fire_data_list.remove(found_fire)
    
    def update(self, fire_data_list, dt):
        """
        """
        for fdat in fire_data_list:
            fdat.radius = taconst.ROBOT_RADIUS / math.sin(math.pi / fdat.intensity)
            
        self._sim_time += dt