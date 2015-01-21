# -*- coding: utf-8 -*-

# ===================================================================
# Base Data Logger
class base_data_logger (object):
    """
    A base class for writing data to file.
    """
    
    # VARIABLES
    file_name = ""    
    file_h = None
    
    # FUNCTIONS  
    def set_file_name(self, file_name):
        self.file_name = file_name
    
    def write_data (self, curr_time, curr_sys_state):
        pass
    
    def close_file(self):
        if self.file_h is not None:
            self.file_h.close()
            self.file_h = None


# ===================================================================
# Mathematica Friendly Data Logger for task allocation experiment
class collab_data_logger (base_data_logger):
    
    def write_data(self, curr_time, curr_sys_state):
        """
        Write data to a file. Output is Mathematica friendly.
        """
        if self.file_h is None:
            self.file_h = open(self.file_name, 'w')
            self.file_h.write("{")
        
        if curr_time == 0:
            self.file_h.write("{%d,%d}"%(curr_time, curr_sys_state["Collaborate"]))
        else:
            self.file_h.write(",\n{%d,%d}"%(curr_time, curr_sys_state["Collaborate"]))
        
    def close_file(self):
        if self.file_h is not None:
            self.file_h.write("}")
            super(collab_data_logger, self).close_file()