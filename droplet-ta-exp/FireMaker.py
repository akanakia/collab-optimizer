# -*- coding: utf-8 -*-
import random

class FireMaker:

    class Cell:   
        # Cell status Enum
        FRONT = 0
        CORE  = 1
        BURNT = 2          
        
        def __init__(self, row, col):
            """
            Cell constructor
            """
            self.col = col
            self.row = row
            self.i = 1
            self.status = FireMaker.Cell.FRONT
            self._allowed_neighbors = None
    
        def get_allowed_neighbors(self, num_cell_rows, num_cell_cols):
            """
            Returns a list of tuples with coordinates of the allowed neighbors of 
            this cell
            """
            if self._allowed_neighbors is None:
                self._allowed_neighbors = []
                
                for colp in [self.col - 1, self.col, self.col + 1]:
                    if self.col - 1 < 0 or self.col + 1 == num_cell_cols:
                        continue
                    for rowp in [self.row - 1, self.row, self.row + 1]:
                        if self.row - 1 < 0 or self.row + 1 == num_cell_rows:
                            continue
                        if self.col == colp and self.row == rowp:
                            continue
                        self._allowed_neighbors.append((colp, rowp))
                        
            return self._allowed_neighbors
    
    
    def __init__(self, cell_height, cell_width, num_cell_rows, num_cell_cols):
        """
        FireMaker Constructor
        """
        self.num_cell_rows = num_cell_rows
        self.num_cell_cols = num_cell_cols
        self.cell_width = cell_width
        self.cell_height = cell_height
        self._active_cells = []

    def add_cell(self, row, col):
        """
        Add a new fire cell placed at location (row, col) on the grid. It
        returns True if a new cell was created, False if a fire cell already 
        existed at that location.
        """
        pass

    def add_cell_random(self):
        """
        Adds a new fire cell randomlly placed on the grid. It will only add a
        new cell if less than 75% of the total area is currently covered by 
        fire. Returns True on success
        """
        if len(self._active_cells) > (self.num_cell_cols * self.num_cell_rows * .75):
            return False
            
        if len(self._active_cells) > 0:
            occupied_cells = [(cell.row, cell.col) for cell in self._active_cells]
            (new_row, new_col) = occupied_cells[0]
            while((new_row, new_col) in occupied_cells):
                (new_row, new_col) = (random.randint(0, self.num_cell_rows - 1), random.randint(0, self.num_cell_cols - 1))
            self._active_cells.append(FireMaker.Cell(new_row, new_col))
        else:
            self._active_cells.append(FireMaker.Cell(random.randint(0, self.num_cell_rows - 1), random.randint(0, self.num_cell_cols - 1)))
            
        return True
    
    def propogate_fire(self):
        """
        Propogates the fire from existing fire cells to neighboring cells using
        the desired probability distribution.
        """
        front_cells = [cell for cell in self._active_cells if cell.status == Cell.FRONT]    
    
    def increment_intensity(self, inc=1):
        """
        Increments the intensity of all the fire cells by the amount specified 
        by inc (=1 by default) up to a max of 255.
        inc souhld be a postive integer.
        """
        for cell in self._active_cells:
            cell.i = min(255, cell.i + inc)

    def get_fire_grid(self):
        """
        Returns a list of the 3-tuples (row, col, intensity) comprising the 
        grid where cells with fire are present
        """
        return [(cell.row, cell.col, cell.i) for cell in self._active_cells]