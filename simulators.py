# -*- coding: utf-8 -*-
from agents import *


# ===================================================================
# Base Task Allocation simulator
class collab_simulator (object):

    # VARIABLES
    num_agents = 0; # PUBLIC
    
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
        self._agent_list = [ collab_agent("Wait") for i in range(self.num_agents) ]
        
        for agent in self._agent_list:
            self._curr_sys_state[agent.get_curr_agent_state()] += 1
    
        self._num_collabs = 0
        self._start_collab_flag = False
    
    def run(self, total_time):       
        """
        Run simulator for total_time steps
        """
        for t in range(total_time):
#            self._data_logger.write_data(t, self._curr_sys_state)

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
#        self._data_logger.close_file()
        
  
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
        self._agent_list = [ noisy_signal_agent("Wait") for i in range(self.num_agents) ]
        
        agent_params_dict['Tau'] = self._noise_signal_val
        self.set_all_agent_params(agent_params_dict)
        
        for agent in self._agent_list:
            self._curr_sys_state[agent.get_curr_agent_state()] += 1
        
        self._num_collabs = 0
        self._start_collab_flag = False
        
    def run(self, total_time):       
        """
        Run simulator for total_time steps
        """
        for t in range(total_time):
#            self._data_logger.write_data(t, self._curr_sys_state)

            # Gather all agents' votes
            vote_state = {"Wait":0, "Collaborate":0}    
            
            # DEBUG CODE HERE
#            print('=========== STEP ' + str(t+1) + ' ============= ')
#            agent_id = 0 
#            for agent in self._agent_list:
#                sys.stdout.write('[Agent ' + str(agent_id) + ': ')
#                vote_state[agent.step(self._curr_sys_state)] += 1
#                print(']')
#                agent_id += 1
            # END DEBUG CODE      

            for agent in self._agent_list:
                vote_state[agent.step(self._curr_sys_state)] += 1
                
            # Change all agents' state to collaborate if majority vote passes
            self._curr_sys_state = {"Wait":0, "Collaborate":0}
            new_state = "Wait"
            if vote_state["Collaborate"] >= vote_state["Wait"]:
                new_state = "Collaborate"
                if self._start_collab_flag:
                    self._num_collabs += 1
                    self._start_collab_flag = False
            else:
                self.set_all_agent_params({'Tau':self._noise_signal_val})
                self._start_collab_flag = True
                
            for agent in self._agent_list:
                self._curr_sys_state[agent.set_curr_agent_state(new_state)] += 1
            
        self._data_logger.write_data(self._num_collabs)
#        self._data_logger.close_file()