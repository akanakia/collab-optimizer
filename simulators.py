# -*- coding: utf-8 -*-

import random
from agents import *


# ===================================================================
# Base Task Allocation simulator
class collab_simulator (object):

    # VARIABLES
    num_agents = 0;
    curr_sys_state = {"Wait":0, "Collaborate":0}        
    data_logger = None;    
    agent_list = None;
 
   
    # FUNCTIONS
    def __init__(self, data_logger):
        self.data_logger = data_logger

    def set_single_agent_params(self, params_dict, agent_id):
        if self.agent_list is not None:
            if agent_id < len(self.agent_list):
                self.agent_list[agent_id].set_params(params_dict)
  
      
    def set_all_agent_params(self, params_dict):        
        if self.agent_list is not None:
            for agent in self.agent_list:
                agent.set_params(params_dict)
    
    
    def reset_run(self):
        """
        Resets the simulation to starting conditions
        """
        self.agent_list = [ collab_agent("Wait") for i in range(self.num_agents) ]
        
        for agent in self.agent_list:
            self.curr_sys_state[agent.get_curr_agent_state()] += 1
    
    
    def run(self, total_time):       
        """
        Run simulator for total_time steps
        """
        for t in range(total_time):
            self.data_logger.write_data(t, self.curr_sys_state)

            # Gather all agents' votes
            vote_state = {"Wait":0, "Collaborate":0}

            for agent in self.agent_list:
                vote_state[agent.step(self.curr_sys_state)] += 1   
                
            # Change all agents' state to collaborate if majority vote passes
            self.curr_sys_state = {"Wait":0, "Collaborate":0}
            new_state = "Wait"
            if vote_state["Collaborate"] >= vote_state["Wait"]:
                new_state = "Collaborate"
            
            for agent in self.agent_list:
                self.curr_sys_state[agent.set_curr_agent_state(new_state)] += 1
            
        self.data_logger.close_file()
        
  
# ===================================================================   
import numpy as np   
class noisy_signal_simulator (collab_simulator):

    # VARIABLES
    _noise_params = {"SignalMean":0, "SignalSD":.1} 
    _noise_signal_val = 0.
    
    # FUNCTIONS
    def __init__(self, data_logger):
        super(noisy_signal_simulator,self).__init__(data_logger)
    
    def reset_signal_noise_params(self,params_dict):
        self._noise_params = params_dict
        self._noise_signal_val = max(np.random.normal(self._noise_params["SignalMean"], self._noise_params["SignalSD"]), 0)               
        
    def reset_run(self,agent_params_dict):
        """
        Resets the simulation to starting conditions
        """
        self.agent_list = [ noisy_signal_agent("Wait") for i in range(self.num_agents) ]
        
        agent_params_dict['Tau'] = self._noise_signal_val
        self.set_all_agent_params(agent_params_dict)
        
        for agent in self.agent_list:
            self.curr_sys_state[agent.get_curr_agent_state()] += 1
            
            
    def run(self, total_time):       
        """
        Run simulator for total_time steps
        """
        for t in range(total_time):
            self.data_logger.write_data(t, self.curr_sys_state)

            # Gather all agents' votes
            vote_state = {"Wait":0, "Collaborate":0}    
            
            # DEBUG CODE HERE
#            print('=========== STEP ' + str(t+1) + ' ============= ')
#            agent_id = 0 
#            for agent in self.agent_list:
#                sys.stdout.write('[Agent ' + str(agent_id) + ': ')
#                vote_state[agent.step(self.curr_sys_state)] += 1
#                print(']')
#                agent_id += 1
            # END DEBUG CODE      

            for agent in self.agent_list:
                vote_state[agent.step(self.curr_sys_state)] += 1
                
            # Change all agents' state to collaborate if majority vote passes
            self.curr_sys_state = {"Wait":0, "Collaborate":0}
            new_state = "Wait"
            if vote_state["Collaborate"] >= vote_state["Wait"]:
                new_state = "Collaborate"
            else:
                self.set_all_agent_params({'Tau':self._noise_signal_val})
                
            for agent in self.agent_list:
                self.curr_sys_state[agent.set_curr_agent_state(new_state)] += 1
            
        self.data_logger.close_file()        