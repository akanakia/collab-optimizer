# -*- coding: utf-8 -*-

#from collab_simulator import collab_simulator
from data_loggers import *
from simulators import *
from agents import *

agent_dist_mean_list = [80, 85, 90, 95, 100, 105, 110, 115, 120]
agent_dist_var_list = [1.]

def collab_run(num_agents, num_runs, run_time):
    """
    """    
    data_logger = large_data_logger()        
    sim = collab_simulator(data_logger)
    sim.num_agents = num_agents
    sim.agent_type = collab_agent
    
    for theta in agent_dist_var_list:
        for tau in agent_dist_mean_list:     

            data_logger.set_file_name('../data/vanilla-theta_' + str(theta) + '-tau_' + str(tau) + '-runtime_' + str(run_time) + '.txt')
            
            for run in range(num_runs):
                sim.reset_run()
                params_dict = {"Theta":theta, "Tau":tau}
                sim.set_all_agent_params(params_dict)
                sim.run(run_time)    
            
            data_logger.close_file()

def noisy_sensor_run(num_agents, num_runs, run_time):
    """
    """
    sensor_noise_sd_list = [1.,2.,5.,10.,20.,50.,100.]
    
    data_logger = large_data_logger()        
    sim = collab_simulator(data_logger)
    sim.num_agents = num_agents
    sim.agent_type = noisy_sensor_agent
    
    for theta in agent_dist_var_list:
        for tau in agent_dist_mean_list:     
            for sensor_sd in sensor_noise_sd_list:                
                data_logger.set_file_name('../data/noisy-theta_' + str(theta) + '-tau_' + str(tau) + '-sensorsd_' + str(sensor_sd) + '-runtime_' + str(run_time) + '.txt')
                for run in range(num_runs):
                    sim.reset_run()
                    params_dict = {"Theta":theta, "Tau":tau, "SensorSD":sensor_sd}
                    sim.set_all_agent_params(params_dict)
                    sim.run(run_time)    
            
                data_logger.close_file()      
                
                
if __name__ == "__main__":
    num_agents = 100
    run_time = 1000
    num_runs = 100

    print('Running Original Collaboration Experiments...')
    collab_run(num_agents, num_runs, run_time)
    print('Done!')
    
    print('Running Noisy Collaboration Experiments...')    
    noisy_sensor_run(num_agents, num_runs, run_time)
    print('Done!')