# -*- coding: utf-8 -*-
import random

class FireMaker:

    class Cell:   
        # Cell status Enum
        UNBURNT = 0
        FRONT   = 1
        CORE    = 2
        BURNT   = 3          
        
        def __init__(self, row, col, num_cell_rows, num_cell_cols):
            """
            Cell constructor. Local variables of this helper class should be 
            treated as READ-ONLY
            """
            self.col = col
            self.row = row
            self.intensity = 1
            self.status = FireMaker.Cell.UNBURNT
            self.neighbors = 0
            
            self.allowed_neighbors = []            
            self._compute_allowed_neighbors(num_cell_rows, num_cell_cols)
    
        def add_num_neighbors(self, n):
            """
            Increments an internal neighbor counter by n. If the internal
            counter becomes greater than max allowed neighbors then the cell's
            state is changed to CORE.
            """
            self.neighbors += n
            if self.neighbors >= len(self.allowed_neighbors):
                self.status = FireMaker.Cell.CORE
        
        def increment_intensity(self, inc):
            """
            Increment the intensity of the fire cell by inc up to a max of 255.
            If the cell reaches max intensity it burns out and it's status is 
            set to BURNT
            """
            self.intensity = min(255, self.intensity + inc)
            if self.intensity == 255:
                self.status = FireMaker.Cell.BURNT
            
        def _compute_allowed_neighbors(self, num_cell_rows, num_cell_cols):
            """
            Returns a list of tuples with coordinates of the allowed neighbors of 
            this cell
            """                
            for colp in [self.col - 1, self.col, self.col + 1]:
                if colp < 0 or colp == num_cell_cols:
                    continue
                for rowp in [self.row - 1, self.row, self.row + 1]:
                    if rowp < 0 or rowp == num_cell_rows:
                        continue
                    if self.col == colp and self.row == rowp:
                        continue
                    self.allowed_neighbors.append((rowp, colp))                  
    
    
    def __init__(self, num_cell_rows, num_cell_cols):
        """
        FireMaker Constructor
        """
        self.num_cell_rows = num_cell_rows
        self.num_cell_cols = num_cell_cols
        self._grid = [[FireMaker.Cell(row, col, num_cell_rows, num_cell_cols) for col in range(num_cell_cols)] for row in range(num_cell_rows)]

    def ignite_cell(self, row, col):
        """
        Add a new fire cell placed at location (row, col) on the grid. It
        returns True if a new cell was created, False if a fire cell already 
        existed at that location.
        """
        if self._grid[row][col].status != FireMaker.Cell.UNBURNT:
            return False
        else:
            self._grid[row][col].status = FireMaker.Cell.FRONT
            return True

    def ignite_cell_random(self):
        """
        Adds a new fire cell randomlly placed on the grid. It will only add a
        new cell if less than 75% of the total area is currently covered by 
        fire. Returns True on success
        """
        unburnt_cells = [cell for cell in self._grid if cell.status == FireMaker.Cell.UNBURNT]
        unburnt_cells[random.randint(0, len(unburnt_cells) - 1)].status = FireMaker.Cell.FRONT
    
    def propogate_fire(self):
        """
        Propogates the fire from existing fire cells to neighboring cells using
        the desired probability distribution.
        """
        front_cells = [cell for cell in self._grid if cell.status == FireMaker.Cell.FRONT]
        for front_cell in front_cells:
            # Check if a front cell has turned into a core cell.
            # This can happen as new cells are added to this loop.
            if front_cell.status != FireMaker.Cell.FRONT:
                continue
            # Roll a dice to see the fire propogates
            if random.random() <= (float(front_cell.i) / 255):
                occupied_cells = [(cell.row, cell.col) for cell in self._grid]
                neighbor_coords = list(front_cell.allowed_neighbors)
                new_firecell_coords = neighbor_coords[random.randint(0, len(neighbor_coords) - 1)]
                while(new_firecell_coords in occupied_cells):
                    neighbor_coords.remove(new_firecell_coords)
                    new_firecell_coords = neighbor_coords[random.randint(0, len(neighbor_coords) - 1)]

                # Add the new cell and update its neighbors' neighbor count
                self.ignite_cell(new_firecell_coords[0], new_firecell_coords[1])
                new_cell = self.get_last_added_cell()
                new_cell_neighbors = [cell for cell in self._grid if (cell.row, cell.col) in new_cell.allowed_neighbors]
                new_cell.add_num_neighbors(len(new_cell_neighbors))
                for cell in new_cell_neighbors:
                    cell.add_num_neighbors(1)            
            
    
    def increment_intensity(self, inc=1):
        """
        Increments the intensity of all the fire cells by the amount specified 
        by inc (=1 by default) up to a max of 255.
        inc souhld be a postive integer.
        """
        burning_cells = [cell for cell in self._grid if (cell.status == FireMaker.Cell.FRONT or cell.status == FireMaker.Cell.CORE)]
        for cell in burning_cells:
            cell.increment_intensity(inc)

    def get_fire_grid(self):
        """
        Returns a list of the 3-tuples (row, col, intensity) comprising the 
        grid where cells with fire are present
        """
        return [(cell.row, cell.col, cell.intensity) for cell in self._grid if cell.status != FireMaker.Cell.UNBURNT]