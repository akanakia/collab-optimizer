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
        if "Theta" in params_dict:
            self._theta = params_dict["Theta"]
        if "Tau" in params_dict:
            self._tau = params_dict["Tau"]

    def _run_sigmoid(self, est):
        vote = 'Wait'
        sig = 1.0 / ( 1.0 + math.exp(self._theta * (self._tau - est)))
        if random.random() <= sig:
            vote = 'Collaborate'
        
        # DEBUG CODE HERE
#        print('SigVal = ' + str(sig) + ' RVal = ' + str(rval) + ' Voted = ' + vote)
        return vote

            
# ===================================================================
# Agent with noisy sensors            
import numpy as np
class noisy_sensor_agent (collab_agent):
    
    # VARIABLES
    _sensor_mean = 0
    _sensor_sd = 0
    
    # FUNCTIONS
    def __init__(self,start_state):
        super(noisy_sensor_agent,self).__init__(start_state)

    def _run_sigmoid(self, est):
        est_noisy = max(est + np.random.normal(self._sensor_mean, self._sensor_sd), 0)
        return super(noisy_sensor_agent, self)._run_sigmoid(est_noisy)
        
    def set_params(self, params_dict):     
        if "SensorMean" in params_dict:
            self._sensor_mean = params_dict["SensorMean"]
        if "SensorSD" in params_dict:
            self._sensor_sd = params_dict["SensorSD"]
        super(noisy_sensor_agent, self).set_params(params_dict)