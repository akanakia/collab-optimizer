# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 19:06:35 2015

This is prototyping the experiment. Task sizes are NOT generated randomly.
The only gaurantee assuming n > 2*m is that sum(k) = n. This is for one of the
three experiment cases I want to run, which are:
    i.   n > sum(k) = Always enough agents for all tasks.
    ii.  n = sum(k) = Exactly enough agents for all tasks.
    iii. n < sum(k) = Never enough agents for all tasks.

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

def generate_k(n, m, expType):
    """
    This function ONLY works if n > 2*m.
    """
    if expType=='NEqualSumK':
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

def generate_d(agent_pos_list, target_pos_list):
    """
    Generates the d matrix
    """
    return [[int(math.hypot(t_pos[0]-a_pos[0],t_pos[1]-a_pos[1])) for t_pos in target_pos_list] for a_pos in agent_pos_list]

def generate_pos_lists(n, m, exp_num, pos_log):
    target_pos_list = [(random.randint(0,ARENA_SIZE),random.randint(0,ARENA_SIZE)) for _ in range(m)]
    agent_pos_list = [(random.randint(0,ARENA_SIZE),random.randint(0,ARENA_SIZE)) for _ in range(n)]
    
    return (agent_pos_list, target_pos_list)     

def plot_results(agent_pos_list, target_pos_list, M, plotID):
    plt.figure(plotID)
    plt.plot(*zip(*target_pos_list), color='red', marker='o', linestyle='')
    plt.plot(*zip(*agent_pos_list), color='blue', marker='x', linestyle='')
    for i in range(NUM_AGENTS):
        for j in range(NUM_TARGETS):
            if M[i][j] == 1:
                plt.plot(*zip(*[agent_pos_list[i], target_pos_list[j]]), color='black', marker='', linestyle='-')
    plt.show()    

def create_log_files(expType):
    """
    expType can be 'equal' 'less' 'greater' referring to the total team 
    requirements for all tasks (sum(k)) vs. number of available agents (n).
    """
    pos_log             = open('PositionLog_'+expType+'.txt', 'w')
    central_ideal_log   = open('CentralIdealExpLog_'+expType+'.txt', 'w')
    central_noisy_log   = open('CentralNoisyExpLog_'+expType+'.txt', 'w')
    distr_noisy_log     = open('DistrNoisyExpLog_'+expType+'.txt', 'w')

    pos_log.write('{\"exp-num\",{\"agent-position-list\"},{\"target-position-list\"}}\n')
    central_ideal_log.write('{\"exp-num\", \"target-teams-sum\", \"num-agents-assigned\", \"num-agents-assigned-successfully\", \"num-targets-assigned\", \"num-targets-assigned-successfully\"}\n')
    central_noisy_log.write('{\"exp-num\", \"target-teams-sum\", \"num-agents-assigned\", \"num-agents-assigned-successfully\", \"num-targets-assigned\", \"num-targets-assigned-successfully\"}\n')
    distr_noisy_log.write  ('{\"exp-num\", \"target-teams-sum\", \"num-agents-assigned\", \"num-agents-assigned-successfully\", \"num-targets-assigned\", \"num-targets-assigned-successfully\"}\n')
    return (pos_log, central_ideal_log, central_noisy_log, distr_noisy_log)

def write_pos_log(agent_pos_list, target_pos_list, exp_num, pos_log):
    pos_log.write('{%d, {'%(exp_num+1))
    pos_log.write('{%d,%d}'%agent_pos_list[0])
    for i in range(1, len(agent_pos_list)):
        pos_log.write(',{%d,%d}'%agent_pos_list[i])
    pos_log.write('},{')
    pos_log.write('{%d,%d}'%target_pos_list[0])
    for i in range(1, len(target_pos_list)):
        pos_log.write(',{%d,%d}'%agent_pos_list[i])    
    pos_log.write('}}\n')
    pos_log.flush()

def write_central_exp_log(k, M, exp_num, central_log):
    target_totals = [sum(col) for col in zip(*M)]
    assigned_targets = 0
    assigned_targets_success = 0
    assigned_agents = 0
    assigned_agents_success = 0
    for i in range(len(target_totals)):
        if target_totals[i] > 0:
            assigned_targets+=1
            assigned_agents+=target_totals[i]
            if target_totals[i] >= k[i]:
                assigned_targets_success+=1
                assigned_agents_success+=target_totals[i]
    
    central_log.write('{%d,%d,%d,%d,%d,%d}\n'%(exp_num+1, sum(k), assigned_agents, assigned_agents_success, assigned_targets, assigned_targets_success))
    central_log.flush()    
    
def write_distr_exp_log(M_dn, exp_num, distr_exp_log):
    pass
    
def run_central_ideal_exp(agent_pos_list, target_pos_list, k, d):
    # The reason for the +1 here is to account for truncation of the 
    # int. It doesn't matter that much in the optimizer so long as 
    # the total welfare is gauranteed to never be negative.
    w = [int(math.hypot(ARENA_SIZE,ARENA_SIZE) * k[i])+1 for i in range(len(k))]
    s = StaticTASolver()
    s.solve(NUM_AGENTS, NUM_TARGETS, k, w, d, ARENA_SIZE/10)
    if s.solution_found:
        (M, W) = s.get_solution()
        return (True, M)
    else:   
        return (False, None)

def run_central_noisy_exp(agent_pos_list, target_pos_list, k, d):
    return (True, None)

def run_distr_noisy_exp(agent_pos_list, target_pos_list, k):
    return (True, None)
    
def run_exps(expType):
    (pos_log, central_ideal_log, central_noisy_log, distr_noisy_log) = create_log_files(expType)
    
    exp_num = 0
    total_attempts = 0
    while exp_num < NUM_EXP:
        # Set up the data used for all experiments here        
        (agent_pos_list, target_pos_list) = generate_pos_lists(NUM_AGENTS, NUM_TARGETS, exp_num, pos_log)
        k = generate_k(NUM_AGENTS, NUM_TARGETS, expType)        
        d = generate_d(agent_pos_list, target_pos_list)
    
        (res_ci, M_ci) = run_central_ideal_exp(agent_pos_list, target_pos_list, k, d)
        (res_cn, M_cn) = run_central_noisy_exp(agent_pos_list, target_pos_list, k, d)
        (res_dn, M_dn) = run_distr_noisy_exp(agent_pos_list, target_pos_list, k)
        
        if (res_ci and res_cn and res_dn):
            write_pos_log(agent_pos_list, target_pos_list, exp_num, pos_log)
            write_central_exp_log(k, M_ci, exp_num, central_ideal_log)
            #write_central_exp_log(k, M_cn, exp_num, central_noisy_log)
            #write_distr_exp_log(M_dn, exp_num, distr_exp_log)
            exp_num+=1

        total_attempts+=1        
        print 'Attempts Complete[%3d] Experiments Complete[%3d]'%(total_attempts, exp_num)
            
    pos_log.close()    
    central_ideal_log.close()
    central_noisy_log.close()
    distr_noisy_log.close()
    
def main():
    run_exps('NEqualSumK')
    #run_exps('NLessSumK')
    #run_exps('NGreateSumK')
    
if __name__=="__main__":
    main()