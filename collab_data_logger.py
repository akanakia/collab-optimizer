# -*- coding: utf-8 -*-

from base_data_logger import base_data_logger

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