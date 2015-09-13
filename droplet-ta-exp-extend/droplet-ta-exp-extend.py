# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from DataHandlers import *
from RobotSimulator import *
from PyGameControl import *
import taconstants as taconst

ARENA_X = 1000 # mm
ARENA_Y = 1000 # mm
SCREEN_X = 1000 # px
SCREEN_Y = 1000 # px
TITLE    = 'robot simulator'
NUM_ROBOTS = 20
NUM_EXPS = 1

def main():

    for exp_num in range(NUM_EXPS):
        rsim = RobotSimulator()
        robot_data_list = rsim.init(NUM_ROBOTS, ((0, ARENA_X), (0, ARENA_Y)))
        
        pg_control = PyGameControl(TITLE, exp_num + 1, SCREEN_X, SCREEN_Y)
        pg_control.init()
        
        while True:
            user_event_list = pg_control.handle_user_events()
            if 'exit' in user_event_list:
                break

            # update the simulator
            rsim.update(robot_data_list, taconst.SIM_TIMESTEP, ((0, ARENA_X), (0, ARENA_Y)))
            
            # Draw robots to screen
            pg_control.draw_robots(robot_data_list, (ARENA_X, ARENA_Y))
            
            # Render to screen
            pg_control.render(fps_lock=False)
            
        pygame.quit()
    
    
if __name__ == "__main__":
    main()