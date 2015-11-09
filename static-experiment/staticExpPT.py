# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 19:06:35 2015

This is prototyping the experiment. Task sizes are NOT generated randomly.
The only gaurantee assuming n > 2*m is that sum(k) = n. This is for the
experiment case I want to run, which is:
    n = sum(k) = Exactly enough agents for all tasks.

@author: Anshul Kanakia
"""
import random
import math
import time
import matplotlib.pyplot as plt

from StaticTASolver import StaticTASolver

################################################################################
NUM_AGENTS  = 20
NUM_TARGETS = 5
ARENA_SIZE  = 1000

NORMAL_VARIANCE = 1

NUM_EXP = 10
MAX_TOTAL_EXP_ATTEMPTS = NUM_EXP * 2

################################################################################
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

def generate_d(agent_pos_list, target_pos_list):
    """
    Generates the |n| x |t| distance matrix
    """
    return [[int(math.hypot(t_pos[0]-a_pos[0],t_pos[1]-a_pos[1])) for t_pos in target_pos_list] for a_pos in agent_pos_list]

def generate_pos_lists(n, m, exp_num, pos_log):
    """
    """
    target_pos_list = [(random.randint(0,ARENA_SIZE),random.randint(0,ARENA_SIZE)) for _ in range(m)]
    agent_pos_list = [(random.randint(0,ARENA_SIZE),random.randint(0,ARENA_SIZE)) for _ in range(n)]
    
    return (agent_pos_list, target_pos_list)     


################################################################################
def plot_results(agent_pos_list, target_pos_list, M, plotID):
    """
    """
    plt.figure(plotID)
    plt.plot(*zip(*target_pos_list), color='red', marker='o', linestyle='')
    plt.plot(*zip(*agent_pos_list), color='blue', marker='x', linestyle='')
    for i in range(NUM_AGENTS):
        for j in range(NUM_TARGETS):
            if M[i][j] == 1:
                plt.plot(*zip(*[agent_pos_list[i], target_pos_list[j]]), color='black', marker='', linestyle='-')
    plt.show()


################################################################################
def create_log_files():
    """
    """
    timestamp = str(int(time.time()))
    
    pos_log             = open('PositionLog_ExpVariance_'       +str(NORMAL_VARIANCE)+'_'+timestamp+'.txt', 'w')
    central_ideal_log   = open('CentralIdealExpLog_ExpVariance_'+str(NORMAL_VARIANCE)+'_'+timestamp+'.txt', 'w')
    central_noisy_log   = open('CentralNoisyExpLog_ExpVariance_'+str(NORMAL_VARIANCE)+'_'+timestamp+'.txt', 'w')
    distr_noisy_log     = open('DistrNoisyExpLog_ExpVariance_'  +str(NORMAL_VARIANCE)+'_'+timestamp+'.txt', 'w')

    pos_log.write('{{\"Agent Positions List\"},{\"Target Positions List\"}}\n')
    central_ideal_log.write('{\"Total Agents\", \"Total Targets\", \"Targets Attempted\", \"Targets Failed\", \"Agents Attempted\", \"Agents Failed\"}\n')
    central_noisy_log.write('{\"Total Agents\", \"Total Targets\", \"Targets Attempted\", \"Targets Failed\", \"Agents Attempted\", \"Agents Failed\"}\n')
    distr_noisy_log.write  ('{\"Total Agents\", \"Total Targets\", \"Targets Attempted\", \"Targets Failed\", \"Agents Attempted\", \"Agents Failed\"}\n')
    return (pos_log, central_ideal_log, central_noisy_log, distr_noisy_log)

def write_pos_log(agent_pos_list, target_pos_list, exp_num, pos_log):
    """
    """
    pos_log.write('{{{%d,%d}'%agent_pos_list[0])
    for i in range(1, len(agent_pos_list)):
        pos_log.write(',{%d,%d}'%agent_pos_list[i])
    pos_log.write('},{')
    pos_log.write('{%d,%d}'%target_pos_list[0])
    for i in range(1, len(target_pos_list)):
        pos_log.write(',{%d,%d}'%agent_pos_list[i])    
    pos_log.write('}}\n')
    pos_log.flush()

def write_exp_log(computed_metrics, log):
    """
    computed_metrics = (attempted_targets, failed_targets, attempted_agents, failed_agents)
    """
    if computed_metrics is None:
        return
    
    log.write('{%d,%d,'%(NUM_AGENTS, NUM_TARGETS))
    log.write('%d,%d,%d,%d}\n'%computed_metrics)
    log.flush()

def compute_metrics(k, M):
    if M is None:
        return
        
    target_totals       = [sum(col) for col in zip(*M)]
    attempted_targets   = sum(target_total > 0 for target_total in target_totals)
    failed_targets      = sum((target_totals[i] > 0 and target_totals[i] < k[i]) for i in range(len(k)))
    attempted_agents    = sum(target_total for target_total in target_totals if target_total > 0)
    failed_agents       = sum(target_totals[i] for i in range(len(k)) if (target_totals[i] > 0 and target_totals[i] < k[i]))
    
    return (attempted_targets, failed_targets, attempted_agents, failed_agents)

################################################################################    
def run_central_exp(agent_pos_list, target_pos_list, k, d):
    """
    """    
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
        
def run_distr_exp(k, k_noisy, M_noisy):
    """
    k_noisy is the noisy team size estimate of tasks used the central noisy experiment.
    M_noisy is the result returned from running the central noisy experiment.
    """
    if M_noisy is None:
        return
        
    target_totals       = [sum(col) for col in zip(*M_noisy)]

    attempted_targets   = 0
    failed_targets      = 0
    attempted_agents    = 0
    failed_agents       = 0
    
    for i in range(len(target_totals)):
        yes_votes = 0
        for agent in range(target_totals[i]):
            agent_mag_sense = max(2, random.normalvariate(0, NORMAL_VARIANCE)+k[i])
            if random.random() <= 1./(1.+math.exp(agent_mag_sense-k_noisy[i])):
                yes_votes += 1
        
        if yes_votes >= k_noisy[i]/2.:
            attempted_targets += 1
            attempted_agents += target_totals[i]
            if target_totals[i] < k[i]:
                failed_targets += 1
                failed_agents += target_totals[i]
                        
    return (attempted_targets, failed_targets, attempted_agents, failed_agents)


################################################################################    
def run_exps():
    """
    """
    (pos_log, central_ideal_log, central_noisy_log, distr_noisy_log) = create_log_files()
    
    exp_num = 0
    total_attempts = 0
    while exp_num < NUM_EXP and total_attempts < MAX_TOTAL_EXP_ATTEMPTS:
        # Set up the data used for all experiments here        
        (agent_pos_list, target_pos_list) = generate_pos_lists(NUM_AGENTS, NUM_TARGETS, exp_num, pos_log)
        k = generate_k(NUM_AGENTS, NUM_TARGETS)        
        d = generate_d(agent_pos_list, target_pos_list)
        
        # RUN CENTRAL IDEAL EXPERIMENT
        (res_ci, M_ci) = run_central_exp(agent_pos_list, target_pos_list, k, d)
        result_metrics_ci = compute_metrics(k, M_ci)

        # RUN CENTRAL NOISY EXPERIMENT
        normal_var = NORMAL_VARIANCE
        k_noisy = [max(2,int(k_i + random.normalvariate(0,normal_var))) for k_i in k]
        (res_cn, M_cn) = run_central_exp(agent_pos_list, target_pos_list, k_noisy, d)
        result_metrics_cn = compute_metrics(k, M_cn)

        # RUN DISTRIBUTED NOISY EXPERIMENT
        result_metrics_dn = run_distr_exp(k, k_noisy, M_cn)
        
        if (res_ci and res_cn):
            write_pos_log(agent_pos_list, target_pos_list, exp_num, pos_log)
            write_exp_log(result_metrics_ci, central_ideal_log)
            write_exp_log(result_metrics_cn, central_noisy_log)
            write_exp_log(result_metrics_dn, distr_noisy_log)
            exp_num+=1

        total_attempts+=1
        print 'Central Ideal: %r | Central Noisy: %r | Distributed Noisy: True'%(res_ci, res_cn)
        print 'Attempts Complete[%3d] Experiments Complete[%3d]'%(total_attempts, exp_num)
            
    pos_log.close()    
    central_ideal_log.close()
    central_noisy_log.close()
    distr_noisy_log.close()

    
def main():
    run_exps()
    
if __name__=="__main__":
    main()