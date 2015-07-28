# -*- coding: utf-8 -*-
from ExperimentController import *

import cProfile as profiler

FPS = 60
SCREEN_X = 720
SCREEN_Y = 760
CELL_W = 1
CELL_H = 1
EXP_TITLE = 'Droplet Collaboration Experiment'

def main():

    ec = ExperimentController(EXP_TITLE, FPS, SCREEN_X, SCREEN_Y, CELL_W, CELL_H)
    if not ec.setup_experiment():
        return
    
    while True:
        user_event_list = ec.handle_user_events()
        if 'exit' in user_event_list:
            break
            
        if not ec.handle_timed_events():
            break
        
        ec.draw_and_wait()

if __name__ == "__main__":
#    profiler.run('main()')
    main()
