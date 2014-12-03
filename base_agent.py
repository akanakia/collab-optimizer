# -*- coding: utf-8 -*-

class base_agent (object):
    
    _curr_agent_state = ""
    
    def __init__(self, start_state):
        self._curr_agent_state = start_state
        pass
    
    def step(self, curr_sys_state):
        """
        simulate a single time step for this agent given the current state of the system.
        Returns the new state of the agent.
        """
        pass
        
    def get_curr_agent_state(self):
        return self._curr_agent_state
        
    def set_curr_agent_state(self, new_state):
        self._curr_agent_state = new_state
        return self.get_curr_agent_state()
        
    def set_params(self, params_dict):
        pass