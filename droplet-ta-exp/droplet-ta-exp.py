# -*- coding: utf-8 -*-
from ExperimentController import *

#import cProfile as profiler

FPS = 60
SCREEN_X = 800
SCREEN_Y = 600 
CELL_W = 4
CELL_H = 4
EXP_TITLE = 'Droplet Collaboration Experiment'

def main():

    ec = ExperimentController(EXP_TITLE, FPS, SCREEN_X, SCREEN_Y, CELL_W, CELL_H)
    if not ec.setup_experiment():
        return
    
    while True:
        user_event_list = ec.handle_user_events()
        if 'exit' in user_event_list:
            break
            
        ec.handle_timed_events()
        ec.draw_and_wait()

if __name__ == "__main__":
#    profiler.run('main()')
    main()