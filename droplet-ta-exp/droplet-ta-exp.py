# -*- coding: utf-8 -*-
import pygame
import random
from pygame.locals import *
import pygame.gfxdraw

FIRE_EXPAND_INTERVAL = .2
FPS = 60

class Cell:

    # Cell status Enum
    FRONT = 0
    CORE  = 1
    BURNT = 2          
    
    def __init__(self, (x_coord, y_coord), i, status):
        self.x = x_coord
        self.y = y_coord
        self.i = i
        self.status = status
        self._max_neighbors = None
        
    def get_max_cell_neighbors(self, (num_cells_x, num_cells_y)):
        if self._max_neighbors is None:
            if (self.x == 0 or self.x == (num_cells_x - 1)) and (self.y == 0 or self.y == (num_cells_y - 1)):
                self._max_neighbors = 3 # corner cell
            elif self.x == 0 or self.x == num_cells_x - 1 or self.y == 0 or self.y == num_cells_y - 1:
                self._max_neighbors = 5 # border cell
            else:
                self._max_neighbors = 8 # internal cell
        
        return self._max_neighbors


def main():
    
    screen_x = 800
    screen_y = 600
    cell_width = 10
    cell_height = 10
    num_cells_x = screen_x / cell_width
    num_cells_y = screen_y / cell_height
    
    # Stores the tuple: ((x, y) , i) where:
    # (x, y) is the coordinate of the cell (0, 0) is top left
    # i is the intensity of a fire cell from 0 to 255. 
    active_cells = [Cell((random.randint(0, num_cells_x - 1),random.randint(0, num_cells_y - 1)), 0, Cell.FRONT)]
    
    pygame.init()
    screen = pygame.display.set_mode((screen_x, screen_y), HWSURFACE | DOUBLEBUF)
    pygame.display.set_caption('Fire Propogation')
    clock = pygame.time.Clock()
    minute_counter = FPS * 60
    
    while (1):        
        # Get user input and data from roborealm
        for event in pygame.event.get():
            # keydown events go here
            if event.type == QUIT:
                pygame.quit()
                return
                
        # Deal with things that happen on minute intervals
        if (minute_counter <= 0):
            minute_counter = FPS * 60
            for cell in active_cells:
                cell.i = min(255, cell.i + 1)
            
        screen.fill((0, 0, 0))        
        
        # Propogate the fire
        
        
        # Draw the fire
        for cell in active_cells:
            screen.fill((255, 255 - cell.i, 0), pygame.Rect((cell.x * cell_width, cell.y * cell_height), (cell_width, cell_height)))
        
        # Render to screen
        pygame.display.flip()

        # 60 fps
        minute_counter -= 1
        clock.tick(FPS)
        
if __name__ == "__main__":
    main()