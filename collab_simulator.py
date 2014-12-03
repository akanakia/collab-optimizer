# -*- coding: utf-8 -*-

from collab_agent import collab_agent

class collab_simulator:

    # VARIABLES
    num_agents = 0;
    curr_sys_state = {"Wait":0, "Collaborate":0}        
    data_logger = None;    
    agent_list = None;
 
   
    # FUNCTIONS
    def __init__(self, data_logger):
        self.data_logger = data_logger
        pass


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

            vote_state = {"Wait":0, "Collaborate":0}            
            for agent in self.agent_list:
                vote_state[agent.step(self.curr_sys_state)] += 1
                
            self.curr_sys_state = {"Wait":0, "Collaborate":0}
            new_state = "Wait"
            if vote_state["Collaborate"] >= vote_state["Wait"]:
                new_state = "Collaborate"
            
            for agent in self.agent_list:
                self.curr_sys_state[agent.set_curr_agent_state(new_state)] += 1
            
        self.data_logger.close_file()