# -*- coding: utf-8 -*-

from collab_simulator import collab_simulator
from collab_data_logger import collab_data_logger

def main():

    data_logger = collab_data_logger()    
    sim = collab_simulator(data_logger)

    theta_list = [0.1, 1.0, 10.0]
    tau_list = range(2, 7)
    
    for run in range(100):
        for theta in theta_list:
            for tau in tau_list:     
                data_logger.set_file_name('data/microsim-theta_' + str(theta) + '-tau_' + str(tau) + '-run_' + str(run+1) + '.txt')
                sim.num_agents = 6
                sim.reset_run()
                params_dict = {"Theta":theta, "Tau":tau}
                sim.set_all_agent_params(params_dict)
                sim.run(30 * 60)    
    

if __name__ == "__main__":
    main()