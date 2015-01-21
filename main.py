# -*- coding: utf-8 -*-

#from collab_simulator import collab_simulator
from data_loggers import *
from simulators import *

def main():
    
    theta_list = [1.0]
    tau_list = [100]
    noise_params = {"signal_mean":6, "signal_var":.1, "sensor_mean":0, "sensor_var":.1}
    data_logger = collab_data_logger()    
    
    sim = noisy_signal_simulator(data_logger, noise_params)
        
    
    for run in range(10):
        for theta in theta_list:
            for tau in tau_list:     
                data_logger.set_file_name('data/' + 'noisy_sensor_sim-' + '-run_' + str(run+1) + '.txt')
                sim.num_agents = 6
                sim.reset_run()
                params_dict = {"Theta":theta, "Tau":tau}
                sim.set_all_agent_params(params_dict)
                sim.run(30 * 60)    
    

if __name__ == "__main__":
    main()