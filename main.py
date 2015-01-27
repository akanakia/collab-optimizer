# -*- coding: utf-8 -*-

#from collab_simulator import collab_simulator
from data_loggers import *
from simulators import *

def collab_run():
    theta_list = [0.1, 1.0, 10.0]
    tau_list = Range(2,7)
    data_logger = collab_data_logger()    
    
    sim = collab_simulator(data_logger)
    sim.num_agents = 6
        
    
    for run in range(10):
        for theta in theta_list:
            for tau in tau_list:     
                data_logger.set_file_name('data/microsim-theta_' + theta + '-tau_' + tau + '-run_' + str(run+1) + '.txt')
                sim.reset_run()
                params_dict = {"Theta":theta, "Tau":tau}
                sim.set_all_agent_params(params_dict)
                sim.run(30 * 60)    
    

def noisy_signal_run():
    theta = 1.0
    signal_noise_mean_list = range(5,16,1)
    signal_noise_sd_list = [.1,.5,1.]
    sensor_noise_sd_list = [.1,.5,1.]
        
    data_logger = collab_data_logger()
    
    sim = noisy_signal_simulator(data_logger)
    sim.num_agents = 10

    for run in range(10):
        for sensor_noise_sd in sensor_noise_sd_list:
            for signal_noise_sd in signal_noise_sd_list:
                for signal_noise_mean in signal_noise_mean_list:     
                    # Set output file name                    
                    data_logger.set_file_name('data/noisysim-sigmean_' + str(signal_noise_mean) + '-signoisesd_' + str(signal_noise_sd) + '-sensorsd_' + str(sensor_noise_sd) + '-run_' + str(run+1) + '.txt')
                    
                    # Set Sensor Error Distribution Parameters
                    params_dict = {"Theta":theta, "SensorMean":0, "SensorSD":sensor_noise_sd}
                    sim.set_all_agent_params(params_dict)                
                    
                    # Set Signal Error Distribution Parameteres
                    params_dict = {"SignalMean":signal_noise_mean, "SignalSD":signal_noise_sd}
                    sim.reset_signal_noise_params(params_dict)
                    
                    # Run simulation
                    sim.reset_run()
                    sim.run(1000)   




if __name__ == "__main__":
    noisy_signal_run()