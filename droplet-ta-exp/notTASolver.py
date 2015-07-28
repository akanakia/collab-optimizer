# -*- coding: utf-8 -*-
import math

class notTASolver:   

    
    
    def get_solution(self):
        return (self._resM, None)
        
    def solve(self, robot_data = {}, target_data = [], k = [], w = [], cst = []):
        """
        Solves the Target Assignemt problem for the given input argunemts:
        robot_data: dict of id: (x, y, theta)
        target_data: list of ((x,y), size)
        k   = List of minimum team size requirements per target. Each entry in
              the list should be a 2-tuple = ((x,y), team-size) where (x,y) is
              the unique target location identifier.
        w   = List of payoffs/welfare per target for a successful assignment. 
              Each entry in the list should be a 2-tuple = ((x,y), base-welfare) 
              where (x,y) is the unique target location identifier.
        cst = List of agent specific target constraints containing the following
              2-tuple format: (a, t) indicating that agent-a CANNOT be assigned
              to target-t.
              
        This function fills a 0/1 n x t matrix-M indicating agent-target
        assignments as well a vector-W of size t indicating the welfare received
        for each successfully assigned target. if no valid assignments are found
        then (M, W) = (None, None)
        """
        
        sorted_indices = sorted(range(len(target_data)),key=lambda x: target_data[x][1], reverse=True)
        sorted_targets = [target_data[i] for i in sorted_indices]
        sorted_k = [k[i] for i in sorted_indices]     
        dist_dict = {target[0]: {robot_id: math.hypot(robot[0:2],target[0]) for (robot_id, robot) in robot_data.items()} for target in target_data}
        
        
        assignments={}
        for target in sorted_k:
            assignments[target[0]]=[]
            num_needed = target[1]
            sorted_dists = sorted(dist_dict[target[0]].items(), key=lambda x: x[1])
            if num_needed > len(sorted_dists):
                continue
            for i in range(num_needed):
                assignments[target[0]].append(sorted_dists[i][0])
                for other_target in sorted_k:
                    if target[0] is not other_target[0]:
                        del dist_dict[other_target[0]][sorted_dists[i][0]]
    
            
                        
        