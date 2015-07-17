# -*- coding: utf-8 -*-
import random

class FireController:

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
            self.allowed_neighbors = []            
            self._compute_allowed_neighbors(num_cell_rows, num_cell_cols)
            
            self.reset_cell_state()
                
        def __hash__(self):
            return hash((self.row, self.col))
            
        def __eq__(self, other):
            return (self.row, self.col) == (other.row, other.col) 

        def reset_cell_state(self):
            self.status = FireController.Cell.UNBURNT
            self.neighbors = 0
            self.intensity = 1
            self.source = None          
            
        def add_num_neighbors(self, n):
            """
            Increments an internal neighbor counter by n. If the internal
            counter becomes greater than max allowed neighbors then the cell's
            state is changed to CORE.
            """
            self.neighbors += n
            if self.neighbors >= len(self.allowed_neighbors):
                self.status = FireController.Cell.CORE
            elif self.neighbors > 0:
                self.status = FireController.Cell.FRONT
        
        def increment_intensity(self, inc):
            """
            Increment the intensity of the fire cell by inc up to a max of 255.
            If the cell reaches max intensity it burns out and it's status is 
            set to BURNT
            """
            self.intensity = min(255, self.intensity + inc)
            if self.intensity == 255:
                self.status = FireController.Cell.BURNT
            
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
        FireController Constructor
        """
        self.num_cell_rows = num_cell_rows
        self.num_cell_cols = num_cell_cols
        self._grid = [[FireController.Cell(row, col, num_cell_rows, num_cell_cols) for col in range(num_cell_cols)] for row in range(num_cell_rows)]
        self._source_cells = {}
        
        self._diff_buffers = [{},{}]
        self._diff_buffer_index = 0
        self._diff_buff = self._diff_buffers[self._diff_buffer_index]        
        
        
        
    def ignite_cell(self, row, col, source=None):
        """
        Add a new fire cell placed at location (row, col) on the grid. It
        returns (True, new cell status) if a new cell was created and
        (False, existince cell status) if a fire cell already existed at that 
        location.
        """
        if self._grid[row][col].status != FireController.Cell.UNBURNT:
            return (False, self._grid[row][col].status)
        else:
            for (nrow, ncol) in self._grid[row][col].allowed_neighbors:
                if self._grid[nrow][ncol].status != FireController.Cell.UNBURNT:
                    self._grid[row][col].add_num_neighbors(1)
                    self._grid[nrow][ncol].add_num_neighbors(1)
                    self._diff_buff[(nrow, ncol)] = (self._grid[nrow][ncol].intensity, self._grid[nrow][ncol].status)

            # If you are the first ever fire cell this might happen        
            if self._grid[row][col].status == FireController.Cell.UNBURNT:
                self._grid[row][col].status = FireController.Cell.FRONT
            
            if source is None:
                self._grid[row][col].source = self._grid[row][col]
                self._source_cells[self._grid[row][col]] = [self._grid[row][col]]
            else:
                self._grid[row][col].source = source
                self._source_cells[source].append(self._grid[row][col])
            
            self._diff_buff[(row, col)] = (self._grid[row][col].intensity, self._grid[row][col].status)
            
            return (True, self._grid[row][col].status)

    def ignite_cell_random(self):
        """
        Adds a new fire cell randomlly placed on the grid. 
        If the new cell has at least 1 UNBURNT neighbor then this function sets 
        the new cell's status to FRONT and returns (True, FRONT). 
        If the new cell has no UNBURNT neighbors left then this functions sets 
        the new cell's status to CORE and returns (True, CORE). 
        Either way a new fire cell is created in a random position on the grid.
        If there are no UNBURNT cell positions left this function returns 
        (False, None)
        """
        unburnt_cells = [cell for gridrows in self._grid for cell in gridrows if cell.status==FireController.Cell.UNBURNT]
        if len(unburnt_cells) == 0:
            return (False, None)
            
        rand_id = random.randint(0, len(unburnt_cells) - 1)
        for (row, col) in unburnt_cells[rand_id].allowed_neighbors:
            if self._grid[row][col].status != FireController.Cell.UNBURNT:
                unburnt_cells[rand_id].add_num_neighbors(1)
                self._grid[row][col].add_num_neighbors(1)
                self._diff_buff[(row, col)] = (self._grid[row][col].intensity, self._grid[row][col].status)
                
        # If you are the first ever fire cell this might happen        
        if unburnt_cells[rand_id].status == FireController.Cell.UNBURNT:
            unburnt_cells[rand_id].status = FireController.Cell.FRONT

        unburnt_cells[rand_id].source = unburnt_cells[rand_id]
        self._source_cells[unburnt_cells[rand_id]] = [unburnt_cells[rand_id]]
        
        self._diff_buff[(unburnt_cells[rand_id].row, unburnt_cells[rand_id].col)] = (unburnt_cells[rand_id].intensity, unburnt_cells[rand_id].status)
        
        return (True, unburnt_cells[rand_id].status)

    def extinguish_fire(self, row, col):
        """
        Extinguishes the entire fire "blob" in the area that cell at pos 
        (row, col) was a part of
        """
        if self._grid[row][col].status != FireController.Cell.UNBURNT:
            source_cell = self._grid[row][col].source
            this_fire_cells = self._source_cells[source_cell]
            for cell in this_fire_cells:
                cell.reset_cell_state()
                self._diff_buff[(cell.row, cell.col)] = (cell.intensity, cell.status)
                
            del self._source_cells[source_cell]
            
    def propogate_fire(self):
        """
        Propogates the fire from existing fire cells to neighboring cells using
        the desired probability distribution.
        """
        front_cells = [cell for gridrows in self._grid for cell in gridrows if cell.status==FireController.Cell.FRONT]
        for front_cell in front_cells:
            # Check if a front cell has turned into a core cell.
            # This can happen as new cells are added to this loop.
            if front_cell.status != FireController.Cell.FRONT:
                continue
            # Roll a dice to see the fire propogates
            if random.random() <= (front_cell.intensity / 255.):
                neighbor_coords = list(front_cell.allowed_neighbors)
                for (row, col) in front_cell.allowed_neighbors:
                    if self._grid[row][col].status != FireController.Cell.UNBURNT:
                        neighbor_coords.remove((row, col))
                (new_cell_row, new_cell_col) = neighbor_coords[random.randint(0, len(neighbor_coords)-1)]
                self.ignite_cell(new_cell_row, new_cell_col, front_cell.source)
            
    
    def increment_intensity(self, inc=1):
        """
        Increments the intensity of all the fire cells by the amount specified 
        by inc (=1 by default) up to a max of 255.
        inc souhld be a postive integer.
        """
        burning_cells = [cell for gridrows in self._grid for cell in gridrows if (cell.status==FireController.Cell.FRONT or cell.status==FireController.Cell.CORE)]
        for cell in burning_cells:
            cell.increment_intensity(inc)
            self._diff_buff[(cell.row, cell.col)] = (cell.intensity, cell.status)

    def get_fire_grid(self):
        """
        Returns a list of the 3-tuples (row, col, intensity) comprising the 
        grid where cells with fire are present
        """
        curr_buff_id = self._diff_buffer_index
        self._diff_buffer_index = (self._diff_buffer_index + 1)%2
        self._diff_buffers[self._diff_buffer_index] = {}
        self._diff_buff = self._diff_buffers[self._diff_buffer_index]
        
        return self._diff_buffers[curr_buff_id]
        
    def get_fire_locations_and_sizes(self):
        """
        Returns the source locations and sizes of currently active fires as a 
        list of 2-tuples: ((row, col), size) or ((y, x), size)
        """
        retval = []
        for source_cell in self._source_cells.keys:
            retval.append((source_cell.row, source_cell.col), len(self._source_cells[source_cell]))
            
        return retval