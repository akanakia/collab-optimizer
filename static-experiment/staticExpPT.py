# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 19:06:35 2015

This is prototyping the experiment. Task sizes are NOT generated randomly.
The only gaurantee assuming n > 2*m is that sum(k) = n. This is for one of the
three experiment cases I want to run, which are:
    i.   n > sum(k) = Always enough robots for all tasks.
    ii.  n = sum(k) = Exactly enough robots for all tasks.
    iii. n < sum(k) = Never enough robots for all tasks.

@author: Anshul Kanakia
"""
import random
import math
import matplotlib.pyplot as plt

from StaticTASolver import StaticTASolver

NUM_AGENTS  = 20
NUM_TARGETS = 5
NUM_EXP     = 100
ARENA_SIZE  = 1000

def generate_k(n, m):
    """
    This function ONLY works if n > 2*m.
    """
    k = [2 for _ in range(m)]
    assign_left = n - (2*m)
    while assign_left > 0:
        if assign_left <= 3:
            k[random.randint(0, m-1)] += assign_left
            assign_left = 0
        else:
            assign = random.randint(1,3)
            k[random.randint(0,m-1)] += assign
            assign_left -= assign

    return k

def generate_pos_lists(n, m, pos_log):
    target_pos_list = [(random.randint(0,ARENA_SIZE),random.randint(0,ARENA_SIZE)) for _ in range(m)]
    agent_pos_list = [(random.randint(0,ARENA_SIZE),random.randint(0,ARENA_SIZE)) for _ in range(n)]
    
    # TODO: Write the position information to the position log file
    
    return (agent_pos_list, target_pos_list)
    
def generate_d(agent_pos_list, target_pos_list):
    """
    Generates the d matrix
    """
    return [[int(math.hypot(t_pos[0]-a_pos[0],t_pos[1]-a_pos[1])) for t_pos in target_pos_list] for a_pos in agent_pos_list]

def plot_results(agent_pos_list, target_pos_list, M, plotID):
    plt.figure(plotID)
    plt.plot(*zip(*target_pos_list), color='red', marker='o', linestyle='')
    plt.plot(*zip(*agent_pos_list), color='blue', marker='x', linestyle='')
    for i in range(NUM_AGENTS):
        for j in range(NUM_TARGETS):
            if M[i][j] == 1:
                plt.plot(*zip(*[agent_pos_list[i], target_pos_list[j]]), color='black', marker='', linestyle='-')
    plt.show()    

def create_log_files(n, m, expType):
    """
    expType can be 'equal' 'less' 'greater' referring to the total team 
    requirements for all tasks (sum(k)) vs. number of available robots (n).
    """
    pos_log             = open('PositionLog_'+expType+'.txt', 'w')
    central_ideal_log   = open('CentralIdealExpLog_'+expType+'.txt', 'w')
    central_noisy_log   = open('CentralNoisyExpLog_'+expType+'.txt', 'w')
    distr_noisy_log     = open('DistrNoisyExpLog_'+expType+'.txt', 'w')
    return (pos_log, central_ideal_log, central_noisy_log, distr_noisy_log)
    
def run_distributed_noisy_exp(agent_pos_list, target_pos_list, k, expNum, distr_noisy_log):
    pass

def run_central_noisy_exp(agent_pos_list, target_pos_list, k, d, expNum, central_noisy_log):
    pass        
        
def run_central_ideal_exp(agent_pos_list, target_pos_list, k, d, expNum, central_ideal_log):
    # The reason for the +1 here is to account for truncation of the 
    # int. It doesn't matter that much in the optimizer so long as 
    # the total welfare is gauranteed to never be negative.
    w = [int(math.hypot(ARENA_SIZE,ARENA_SIZE) * k[i])+1 for i in range(len(k))]
    s = StaticTASolver()
    s.solve(NUM_AGENTS, NUM_TARGETS, k, w, d, ARENA_SIZE/10)
    if s.solution_found:
        print 'Solution: FOUND'
        (M, W) = s.get_solution()
        plot_results(agent_pos_list, target_pos_list, M, expNum)
    else:
        print 'Solution: NOT FOUND'    
    
def run_exps(expType):
    (pos_log, central_ideal_log, central_noisy_log, distr_noisy_log) = create_log_files(expType)
    
    for expNum in range(NUM_EXP):
        # Set up the data used for all experiments here        
        k = generate_k(NUM_AGENTS, NUM_TARGETS, expType)
        (agent_pos_list, target_pos_list) = generate_pos_lists(NUM_AGENTS, NUM_TARGETS, pos_log)       
        d = generate_d(agent_pos_list, target_pos_list)
    
        run_central_ideal_exp(agent_pos_list, target_pos_list, k, d, expNum, central_ideal_log)
        run_central_noisy_exp(agent_pos_list, target_pos_list, k, d, expNum, central_noisy_log)
        run_distributed_noisy_exp(agent_pos_list, target_pos_list, k, expNum, distr_noisy_log)
            
def main():
    run_exps('NEqualSumK')
    run_exps('NLessSumK')
    run_exps('NGreateSumK')
    
if __name__=="__main__":
    main()