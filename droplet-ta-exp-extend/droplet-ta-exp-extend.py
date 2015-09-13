# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from DataHandlers import *
from RobotSimulator import *
from FireSimulator import *
from PyGameControl import *
import taconstants as taconst

ARENA_X = 1000 # mm
ARENA_Y = 1000 # mm
SCREEN_X = 1000 # px
SCREEN_Y = 1000 # px
TITLE    = 'robot simulator'

NUM_ROBOTS = 20
NUM_START_FIRES = 4
NUM_EXPS = 1

def main():

    for exp_num in range(NUM_EXPS):
        sim_time = 0.
        
        rsim = RobotSimulator()
        robot_data_list = rsim.init(NUM_ROBOTS, ((0, ARENA_X), (0, ARENA_Y)))
        
        fsim = FireSimulator()
        fire_data_list = fsim.init(NUM_START_FIRES, ((0, ARENA_X), (0, ARENA_Y)))
        
        
        pg_control = PyGameControl(TITLE, exp_num + 1, SCREEN_X, SCREEN_Y)
        pg_control.init()
        
        while True:
            # handle user events
            user_event_list = pg_control.handle_user_events()
            if 'exit' in user_event_list:
                break

            # update the simulators
            fsim.update(fire_data_list, taconst.SIM_TIMESTEP)
            rsim.update(robot_data_list, taconst.SIM_TIMESTEP, ((0, ARENA_X), (0, ARENA_Y)))
            
            # Draw objects to screen
#            pg_control.draw_fire(fire_data_list, (ARENA_X, ARENA_Y))
#            pg_control.draw_robots(robot_data_list, (ARENA_X, ARENA_Y))
            pg_control.draw_fire(fire_data_list)
            pg_control.draw_robots(robot_data_list)            
            # Render to screen
            pg_control.render(fps_lock=False)
            sim_time += taconst.SIM_TIMESTEP
            
        pygame.quit()
    
    
if __name__ == "__main__":
    main()