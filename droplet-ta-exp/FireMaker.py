# -*- coding: utf-8 -*-
import random

class FireMaker:

    class Cell:   
        # Cell status Enum
        FRONT = 0
        CORE  = 1
        BURNT = 2          
        
        def __init__(self, row, col, num_cell_rows, num_cell_cols):
            """
            Cell constructor
            """
            self.col = col
            self.row = row
            self.i = 1
            self.status = FireMaker.Cell.FRONT
            self._compute_allowed_neighbors(num_cell_rows, num_cell_cols)
            self._num_neighbors = 0
    
        def add_num_neighbors(self, n):
            """
            Increments an internal neighbor counter by n. If the internal
            counter becomes greater than max allowed neighbors then the cell's
            state is changed to CORE.
            """
            self._num_neighbors += n
            if self._num_neighbors >= len(self.allowed_neighbors):
                self.status = FireMaker.Cell.CORE
            
        def _compute_allowed_neighbors(self, num_cell_rows, num_cell_cols):
            """
            Returns a list of tuples with coordinates of the allowed neighbors of 
            this cell
            """
            self.allowed_neighbors = []
                
            for colp in [self.col - 1, self.col, self.col + 1]:
                if colp < 0 or colp == num_cell_cols:
                    continue
                for rowp in [self.row - 1, self.row, self.row + 1]:
                    if rowp < 0 or rowp == num_cell_rows:
                        continue
                    if self.col == colp and self.row == rowp:
                        continue
                    self.allowed_neighbors.append((rowp, colp))                  
    
    
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
        if len(self._active_cells) > 0:
            occupied_cells = [(cell.row, cell.col) for cell in self._active_cells]
            if (row, col) in occupied_cells:
                return False

        self._active_cells.append(FireMaker.Cell(row, col, self.num_cell_rows, self.num_cell_cols))
        return True

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
            self._active_cells.append(FireMaker.Cell(new_row, new_col, self.num_cell_rows, self.num_cell_cols))
        else:
            self._active_cells.append(FireMaker.Cell(random.randint(0, self.num_cell_rows - 1), random.randint(0, self.num_cell_cols - 1), self.num_cell_rows, self.num_cell_cols))
            
        return True
        
    def get_last_added_cell(self):
        if len(self._active_cells) > 0:
            return self._active_cells[len(self._active_cells) - 1]
        else:
            return None
    
    def propogate_fire(self):
        """
        Propogates the fire from existing fire cells to neighboring cells using
        the desired probability distribution.
        """
        new_cell_added = False
        front_cells = [cell for cell in self._active_cells if cell.status == FireMaker.Cell.FRONT]
        for front_cell in front_cells:
            # Roll a dice to see the fire propogates
            if random.random() <= (float(front_cell.i) / 255):
                occupied_cells = [(cell.row, cell.col) for cell in self._active_cells]
                neighbor_coords = list(front_cell.allowed_neighbors)
                new_firecell_coords = neighbor_coords[random.randint(0, len(neighbor_coords) - 1)]
                while(new_firecell_coords in occupied_cells):
                    neighbor_coords.remove(new_firecell_coords)
                    new_firecell_coords = neighbor_coords[random.randint(0, len(neighbor_coords) - 1)]

                self.add_cell(new_firecell_coords[0], new_firecell_coords[1])
                new_cell_added = True
        
        # If a new cell was added then check if any FRONT cells need to become 
        # CORE cells
        if new_cell_added:
            new_cell = self.get_last_added_cell()
            new_cell_neighbors = [cell for cell in front_cells if (cell.row, cell.col) in new_cell.allowed_neighbors]
            new_cell.add_num_neighbors(len(new_cell_neighbors))
            for cell in new_cell_neighbors:
                cell.add_num_neighbors(1)
            
            
    
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