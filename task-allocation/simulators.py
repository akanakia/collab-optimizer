# -*- coding: utf-8 -*-
from agents import *


# ===================================================================
# Base Task Allocation simulator
class collab_simulator (object):

    # VARIABLES
    num_agents = 0 # PUBLIC
    agent_type = None
    
    _curr_sys_state = {"Wait":0, "Collaborate":0}        
    _data_logger = None
    _agent_list = None
    _num_collabs = 0
    _start_collab_flag = False
    
    # FUNCTIONS
    def __init__(self, data_logger):
        self._data_logger = data_logger

    def set_single_agent_params(self, params_dict, agent_id):
        if self._agent_list is not None:
            if agent_id < len(self._agent_list):
                self._agent_list[agent_id].set_params(params_dict)
  
      
    def set_all_agent_params(self, params_dict):        
        if self._agent_list is not None:
            for agent in self._agent_list:
                agent.set_params(params_dict)
    
    
    def reset_run(self):
        """
        Resets the simulation to starting conditions
        """
        if (self.agent_type is None) or (self.num_agents == 0):
            print 'Set agent type and number of agents first.'
            return 
        
        self._agent_list = [self.agent_type("Wait") for i in range(self.num_agents)]
        
        for agent in self._agent_list:
            self._curr_sys_state[agent.get_curr_agent_state()] += 1
    
        self._num_collabs = 0
        self._start_collab_flag = False
    
    def run(self, total_time):       
        """
        Run simulator for total_time steps
        """
        for t in range(total_time):
            # Gather all agents' votes
            vote_state = {"Wait":0, "Collaborate":0}

            for agent in self._agent_list:
                vote_state[agent.step(self._curr_sys_state)] += 1   
                
            new_state = "Wait"
            if vote_state["Collaborate"] >= vote_state["Wait"]:
                new_state = "Collaborate"                
                if self._start_collab_flag:
                    self._num_collabs += 1
                    self._start_collab_flag = False
            else:
                self._start_collab_flag = True

            self._curr_sys_state = {"Wait":0, "Collaborate":0}            
            for agent in self._agent_list:
                self._curr_sys_state[agent.set_curr_agent_state(new_state)] += 1
            
        self._data_logger.write_data(self._num_collabs)