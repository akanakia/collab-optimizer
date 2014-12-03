# -*- coding: utf-8 -*-
import math
import random
from base_agent import base_agent

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