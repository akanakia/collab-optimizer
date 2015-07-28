# -*- coding: utf-8 -*-
from ExperimentController import *

import time
import cProfile as profiler

FPS = 60
SCREEN_X = 720
SCREEN_Y = 760
CELL_W = 1
CELL_H = 1
EXP_TITLE = 'Droplet Collaboration Experiment'
NUM_EXP = 1
EXP_TIME = 60 * 60 # 1 hour long experiments
COM_PORT = 'COM16'

def run_exp(exp_num):
    start_time = time.time()
    ec = ExperimentController(EXP_TITLE, exp_num, FPS, SCREEN_X, SCREEN_Y, CELL_W, CELL_H)
    if not ec.setup_experiment(COM_PORT):
        ec.terminate_exp()
        return
    
    while time.time() - start_time <= EXP_TIME:
        user_event_list = ec.handle_user_events()
        if 'exit' in user_event_list:
            break
            
        if not ec.handle_timed_events():
            break
        
        ec.draw_and_wait()
    
    ec.terminate_exp()

def main():
    for exp_num in range(NUM_EXP):
        run_exp(exp_num+1)

if __name__ == "__main__":
#    profiler.run('main()')
    main()
