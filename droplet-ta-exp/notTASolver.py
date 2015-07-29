# -*- coding: utf-8 -*-
import math

class notTASolver:   
    def get_solution(self):
        return (self.assignments, None)
        
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
        """
        
        sorted_k = sorted(k, key=lambda c: c[1])
        dist_dict = {target_pos: {robot_id: math.hypot(robot[0:2],target_pos) for (robot_id, robot) in robot_data.items()} for (target_pos, target_size) in target_data}
        
        
        self.assignments={}
        for (target_pos, target_team_size) in sorted_k:
            self.assignments[target_pos]=[]
            sorted_dists = sorted(dist_dict[target_pos].items(), key=lambda x: x[1])
            if target_team_size > len(sorted_dists):
                continue
            for i in range(target_team_size):
                self.assignments[target_pos].append(sorted_dists[i][0])
                for (other_target_pos, other_target_team_size) in sorted_k:
                    if target_pos is not other_target_pos:
                        del dist_dict[other_target_pos][sorted_dists[i][0]]