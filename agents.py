# -*- coding: utf-8 -*-
import math
import random

# ===================================================================
# Base Agent
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


# ===================================================================
# Original Task Allocation algorithm agent
class collab_agent (base_agent):

    # VARIABLES
    _collab_time = 5
    _task_time = 0
    _theta = 0.0
    _tau = 0
    
    # FUNCTIONS
    def __init__(self, start_state):
        super(collab_agent,self).__init__(start_state)
    
    def step(self, curr_sys_state):
        if self._curr_agent_state == "Wait":
            return self._run_sigmoid(curr_sys_state["Wait"])
        else:
            self._task_time += 1
            if self._task_time >= self._collab_time:
                self._task_time = 0
                return "Wait"
            else:
                return "Collaborate"
            
    def set_params(self, params_dict):
        self._theta = params_dict["Theta"]
        self._tau = params_dict["Tau"]

    def _run_sigmoid(self, est):
        sig = 1.0 / ( 1.0 + math.exp(self._theta * (self._tau - est)))
        if random.random() <= sig:
            return "Collaborate"
        else:
            return "Wait"

            
# ===================================================================
# Agent with noisy sensors            
class noisy_signal_agent (collab_agent):
    
    # VARIABLES
    _sensor_mean = 0
    _sensor_sd = 0
    
    # FUNCTIONS
    def __init__(self,start_state):
        super(noisy_signal_agent,self).__init__(start_state)
        
    def set_params(self, params_dict):     
        if "SensorMean" in params_dict:
            self._sensor_mean = params_dict["SensorMean"]
        if "SensorSD" in params_dict:
            self._sensor_sd = params_dict["SensorSD"]
        if "Theta" in params_dict:
            self._theta = params_dict["Theta"]
        if "Tau" in params_dict:
            noisy_sensor_val = random.normalvariate(self._sensor_mean, self._sensor_sd)
            self._tau = params_dict["Tau"] + noisy_sensor_val