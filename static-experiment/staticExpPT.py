# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 19:06:35 2015

This is prototyping the experiment. Task sizes are NOT generated randomly.
The only gaurantee assuming n > 2*m is that sum(k) = n. This is for one of the
three experiment cases I want to run, which are:
    i.   n > sum(k) = Always enough robots for all tasks.
    ii.  n = sum(k) = Exactly enough robots for all tasks.
    iii. n < sum(k) = Never enough robots for all tasks.

@author: admin
"""
import random
import math
import matplotlib.pyplot as plt

from StaticTASolver import StaticTASolver

ARENA_SIZE = 1000

def generate_k(n,m):
    """
    This function ONLY works if n > 2*m.
    """
    k = [2 for _ in range(m)]
    for _ in range(n - (2*m)):
        k[random.randint(0, m-1)] += 1

    return k

def generate_d(n, m):
    """
    Generates the d matrix
    """
    target_pos_list = [(random.randint(0,ARENA_SIZE),random.randint(0,ARENA_SIZE)) for _ in range(m)]
    agent_pos_list = [(random.randint(0,ARENA_SIZE),random.randint(0,ARENA_SIZE)) for _ in range(n)]
    
    return (agent_pos_list, target_pos_list, [[int(math.hypot(t_pos[0]-a_pos[0],t_pos[1]-a_pos[1])) for t_pos in target_pos_list] for a_pos in agent_pos_list])

def n_equals_sum_k():
    n = 20
    m = 5
    numExp = 1
    
    for expID in range(numExp):
        k = generate_k(n,m)
        (agent_pos_list, target_pos_list, d) = generate_d(n,m)
        
        # The reason for the +1 here is to account for truncation of the 
        # int. It doesn't matter that much in the optimizer so long as 
        # the total welfare is gauranteed to never be negative.
        w = [int(math.hypot(ARENA_SIZE,ARENA_SIZE) * k[i])+1 for i in range(len(k))]
        s = StaticTASolver()
        s.solve(n,m,k,w,d,ARENA_SIZE/10)
        if s.solution_found:
            print 'Solution: FOUND'
            (M, W) = s.get_solution()
            plt.plot(*zip(*target_pos_list), color='red', marker='o', linestyle='')
            plt.plot(*zip(*agent_pos_list), color='blue', marker='x', linestyle='')
            for i in range(n):
                for j in range(m):
                    if M[i][j] == 1:
                        plt.plot(*zip(*[agent_pos_list[i], target_pos_list[j]]), color='black', marker='', linestyle='-')
            plt.show()
        else:
            print 'Solution: NOT FOUND'

def n_greater_than_sum_k():
    pass

def n_less_than_sum_k():
    pass


def main():
    n_equals_sum_k()

if __name__=="__main__":
    main()