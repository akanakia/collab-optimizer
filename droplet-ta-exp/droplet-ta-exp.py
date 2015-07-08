# -*- coding: utf-8 -*-
import pygame
from FireMaker import *

FPS = 60
SCREEN_X = 800
SCREEN_Y = 600    
CELL_W = 2
CELL_H = 2

def main():

    # Set up the FireMaker class and add a randomly located fire seed
    fm = FireMaker(CELL_H, CELL_W, SCREEN_Y / CELL_H, SCREEN_X / CELL_W)
    fm.add_cell_random()
    
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

        # Clear the screen            
        screen.fill((0, 0, 0))  

        # Minute interval
        if minute_counter > (FPS * 60):
            minute_counter = 1
                
        # 20 second interval
        if (minute_counter % (FPS * 5)) == 0:
            fm.increment_intensity(5)
            
        # Propogate the fire
        fm.propogate_fire()
        
        # Draw the fire
        for (y_pos, x_pos, intensity) in fm.get_fire_grid():
            screen.fill((255, 255 - intensity, 0), pygame.Rect((x_pos * fm.cell_width, y_pos * fm.cell_height), (fm.cell_width, fm.cell_height)))
        
        # Render to screen
        pygame.display.flip()

        # 60 fps
        minute_counter += 1
        clock.tick(FPS)
        
if __name__ == "__main__":
    main()