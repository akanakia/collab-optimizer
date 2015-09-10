# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 19:58:10 2015

@author: admin
"""

import pygame
from pygame.locals import *
from RobotData import *
from RobotSimulator import *
import random
import math

ROBOT_RADIUS = 15 # mm or px, the ratio is 1:1 for now
FPS = 60

def mm_to_px(mm_x, mm_y):
    return (int(mm_x), int(mm_y))

def main(screen_x, screen_y, title):
    # Set up PyGame
    pygame.init()
    screen = pygame.display.set_mode((screen_x, screen_y), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    screen.fill((0,0,0))
    
    robot_data_list = [RobotData((random.randint(ROBOT_RADIUS, screen_x - ROBOT_RADIUS), random.randint(ROBOT_RADIUS, screen_y - ROBOT_RADIUS)), (30 * i)%360, i, 'TURN_LEFT') for i in range(20)]

    # Create robot simulator object
    rsim = RobotSimulator()
    
    while True:
        event_type = ''
        for event in pygame.event.get():
            # keydown events go here
            if event.type == QUIT:
                event_type = 'quit'
                break
                
        if event_type == 'quit':
            break
        
        screen.fill((0,0,0))

        # update the simulator
        rsim.update(robot_data_list, 1000.0/FPS, ((ROBOT_RADIUS, screen_x - ROBOT_RADIUS),(ROBOT_RADIUS, screen_y - ROBOT_RADIUS)))
        
        # Draw robots to screen
        for rdat in robot_data_list:
            (px_x, px_y) = mm_to_px(rdat.x, rdat.y)
            pygame.draw.circle(screen, rdat.simonly_color, (px_x, px_y), rdat.simonly_rad, 1)
            pygame.draw.circle(screen, (100, 100, 100), (px_x, px_y), rdat.simonly_rad - 1) 
            pygame.draw.line(screen, rdat.simonly_color, (px_x, px_y), (px_x + int(rdat.simonly_rad * math.cos(rdat.orient_rad())), px_y + int(rdat.simonly_rad * math.sin(rdat.orient_rad()))))      
        
        # Render to screen
        pygame.display.flip()
        clock.tick()
        
    pygame.quit()
    
    
if __name__ == "__main__":
    screen_x = 1000
    screen_y = 1000
    title    = 'robot simulator'
    main(screen_x, screen_y, title)