# -*- coding: utf-8 -*-

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