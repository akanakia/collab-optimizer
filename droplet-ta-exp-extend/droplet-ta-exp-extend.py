# -*- coding: utf-8 -*-
import math

from DataHandlers import ExpData
from RobotSimulator import RobotSimulator
from FireSimulator import FireSimulator
from PyGameControl import PyGameControl
from TASolver import TASolver
from ActionCommandControl import ActionCommandControl
import taconstants as taconst

ARENA_X = 1000 # mm
ARENA_Y = 1000 # mm
SCREEN_X = 720 # px
SCREEN_Y = 760 # px
TITLE    = 'robot simulator'

NUM_ROBOTS = 20
NUM_START_FIRES = 3
NUM_EXPS = 1
EXP_LENGTH = 1000 * 60 * 60 # 1 hour in ms

def generate_allocations(robot_data_list, fire_data_list, exp_data):
           
    n = len(robot_data_list)
    t = len(fire_data_list)
    k = [((fdat.x, fdat.y), fdat.intensity - len(fdat.curr_team)) for fdat in fire_data_list]
    w = [((fdat.x, fdat.y), fdat.intensity) for fdat in fire_data_list]
    cst_zero = []
    cst_one  = []
    for i in range(n):
        if robot_data_list[i].action == 'WAITING' or robot_data_list[i] == 'LED_ON':
            cst_zero += [(i, j) for j in range(t)]
    d = [[round(exp_data.D[i][j]/math.hypot(ARENA_X, ARENA_Y),2) for j in range(t)] for i in range(n)]
    
    solver = TASolver()
    if solver.solve(n,t,k,w,cst_zero,cst_one,d) > 0:
        (M, W) = solver.get_solution()
        for i, row in enumerate(M):
            if 1 in row:
                robot_data_list[i].target_coords = (fire_data_list[row.index(1)].x, fire_data_list[row.index(1)].y)
                
#                fire_data_list[row.index(1)].curr_team.append(robot_data_list[i].robot_id)

def main():
    for exp_num in range(NUM_EXPS):
        sim_time = 0.
        
        rsim = RobotSimulator()
        robot_data_list = rsim.init(NUM_ROBOTS, ((0, ARENA_X), (0, ARENA_Y)))
        
        fsim = FireSimulator()
        fire_data_list = fsim.init(NUM_START_FIRES, ((0, ARENA_X), (0, ARENA_Y)))
        
        exp_data = ExpData()    
        
        pg_control = PyGameControl(TITLE, exp_num + 1, SCREEN_X, SCREEN_Y)
        pg_control.init()

        fpslock = False
        while sim_time <= EXP_LENGTH:
            # handle user events
            user_event_list = pg_control.handle_user_events()
            if 'exit' in user_event_list:
                break
            for event in user_event_list:
                if 'key-down' in event:
                    (event_type, event_data) = event
                    if event_data == 'l':
                        fpslock = not fpslock

            # Handle timed events            
            #3 minute events
            if sim_time % (1000 * 60 * 3) < taconst.SIM_TIMESTEP:
                fsim.start_fire(fire_data_list,((0, ARENA_X),(0, ARENA_Y)))
                exp_data.set_distance_matrix(robot_data_list, fire_data_list)
                
            # 3 second events
            if sim_time % (1000 * 3) < taconst.SIM_TIMESTEP: 
                exp_data.set_distance_matrix(robot_data_list, fire_data_list)
                action_control = ActionCommandControl()                
                action_control.generate_robot_actions(robot_data_list, fire_data_list)
                
            # 30 second events
            if sim_time % (1000 * 30) < taconst.SIM_TIMESTEP:
                # Call the TASolver
                generate_allocations(robot_data_list, fire_data_list, exp_data)

            # update the simulators
            fsim.update(fire_data_list)
            rsim.update(robot_data_list, ((0, ARENA_X), (0, ARENA_Y)))
            
            # Draw objects to screen
            pg_control.draw_fire(fire_data_list, (ARENA_X, ARENA_Y))
            pg_control.draw_robots(robot_data_list, (ARENA_X, ARENA_Y))
            
            # Render to screen
            pg_control.render(fps_lock=fpslock)
            sim_time += taconst.SIM_TIMESTEP
            
        pg_control.quit()
    
    
if __name__ == "__main__":
    main()