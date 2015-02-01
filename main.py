# -*- coding: utf-8 -*-

#from collab_simulator import collab_simulator
from data_loggers import *
from simulators import *

def collab_run(num_agents, num_runs, run_time):
    theta_list = [1.0]
    tau_list = [5,8,9,10,11,12,15]
    data_logger = collab_data_logger()    
    
    sim = collab_simulator(data_logger)
    sim.num_agents = num_agents
        
    
    for run in range(num_runs):
        for theta in theta_list:
            for tau in tau_list:     
                data_logger.set_file_name('data/microsim-theta_' + str(theta) + '-tau_' + str(tau) + '-run_' + str(run+1) + '.txt')
                sim.reset_run()
                params_dict = {"Theta":theta, "Tau":tau}
                sim.set_all_agent_params(params_dict)
                sim.run(run_time)    
    

def noisy_signal_run(num_agents, num_runs, run_time):
    theta = 1.0
    signal_noise_mean_list = [5,8,9,10,11,12,15]
    signal_noise_sd_list = [.1,1.,2.,5.,10.]
    sensor_noise_sd_list = [.1,1.,2.,5.,10.]
        
    # DEBUGGING
#    signal_noise_mean_list = range(15,16,1)
#    signal_noise_sd_list = [1.]
#    sensor_noise_sd_list = [1.]
    
    data_logger = collab_data_logger()
    
    sim = noisy_signal_simulator(data_logger)
    sim.num_agents = num_agents

    for run in range(num_runs):
        for sensor_noise_sd in sensor_noise_sd_list:
            for signal_noise_sd in signal_noise_sd_list:
                for signal_noise_mean in signal_noise_mean_list:     
                    # Set output file name                    
                    data_logger.set_file_name('data/noisysim-sigmean_' + str(signal_noise_mean) + '-signoisesd_' + str(signal_noise_sd) + '-sensorsd_' + str(sensor_noise_sd) + '-run_' + str(run+1) + '.txt')
                    
                    # Set Signal Error Distribution Parameteres
                    params_dict = {"SignalMean":signal_noise_mean, "SignalSD":signal_noise_sd}
                    sim.reset_signal_noise_params(params_dict)
                    # Call to initialize agent list in simulator                    
                    agent_params_dict = {"Theta":theta, "SensorMean":0, "SensorSD":sensor_noise_sd}
                    sim.reset_run(agent_params_dict)             
                    
                    # Run simulation
                    sim.run(run_time)      

if __name__ == "__main__":
    num_agents = 10     
    run_time = 1000
    num_runs = 10

    print('Running Original Collaboration Experiments...')
    collab_run(num_agents, num_runs, run_time)
    print('Done!')
    
    print('Running Noisy Collaboration Experiments...')    
    noisy_signal_run(num_agents, num_runs, run_time)
    print('Done!')