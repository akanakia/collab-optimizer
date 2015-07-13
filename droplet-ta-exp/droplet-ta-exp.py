# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from FireMaker import *

FPS = 60
SCREEN_X = 800
SCREEN_Y = 600    
CELL_W = 4
CELL_H = 4

def main():

    # Set up the FireMaker class and add a randomly located fire seed
    fm = FireMaker(SCREEN_Y / CELL_H, SCREEN_X / CELL_W)
    (retval, state) = fm.ignite_cell_random()
    if not retval:
        print('Problem initializing fire grid.')
        return
    
    # Set up PyGame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption('Fire Propogation')
    clock = pygame.time.Clock()
    minute_counter = 1
    
    while (1):        
        # Get user input and data from roborealm
        for event in pygame.event.get():
            # keydown events go here
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == MOUSEBUTTONUP:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()
                fm.ignite_cell(mouse_y/CELL_H, mouse_x/CELL_W)
                
        # Clear the screen            
        screen.fill((0, 0, 0))  

        # Minute interval
        if minute_counter > (FPS * 60):
            minute_counter = 1
                
        # 20 second interval
        if (minute_counter % (FPS * 5)) == 0:
            fm.increment_intensity(5)
            
        # random interval
        if random.randint(0, FPS * 2) == 0:
            fm.increment_intensity(5)
            
        # Propogate the fire
        fm.propogate_fire()
        
        # Draw the fire
        for (y_pos, x_pos, intensity, status) in fm.get_fire_grid():
            if status==FireMaker.Cell.FRONT:
                screen.fill((0, 0, 255), pygame.Rect((x_pos * CELL_W, y_pos * CELL_H), (CELL_W, CELL_H)))
            else:
                screen.fill((255, 255 - intensity, 0), pygame.Rect((x_pos * CELL_W, y_pos * CELL_H), (CELL_W, CELL_H)))
        
        # Render to screen
        pygame.display.flip()

        # 60 fps
        minute_counter += 1
        clock.tick(FPS)
        
if __name__ == "__main__":
    main()