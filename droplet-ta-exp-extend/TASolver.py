# -*- coding: utf-8 -*-
import z3

import taconstants as taconst

class TASolver:
    def get_solution(self):
        return (self._resM, self._resW)
        
    def solve(self, n = 0, t = 0, k = [], w = [], cst = [], d = []):
        """
        Solves the Target Assignemt problem for the given input argunemts:
        n   = Number of agents.
        t   = Number of targets.
        k   = List of minimum team size requirements per target. Each entry in
              the list should be a 2-tuple = ((x,y), team-size) where (x,y) is
              the unique target location identifier.
        w   = List of payoffs/welfare per target for a successful assignment. 
              Each entry in the list should be a 2-tuple = ((x,y), base-welfare) 
              where (x,y) is the unique target location identifier.
        cst = List of agent specific target constraints containing the following
              2-tuple format: (a, t) indicating that agent-a CANNOT be assigned
              to target-t.
        d   = The |N| x |T| distance-payoff matrix. The values d_{ij} in this 
              matrix should contain the normalized penalty for assigning agent
              i to target j. All values in this matrix should be non-negative.
              
        This function fills a 0/1 n x t matrix-M indicating agent-target
        assignments as well a vector-W of size t indicating the welfare received
        for each successfully assigned target. if no valid assignments are found
        then (M, W) = (None, None)
        """        
        # Setup initial constraints & add a backtracking point
        self._set_ta_vars(n, t, k, w, cst, d)
        self._init_model()

        # If there are no targets return immediately        
        if t == 0 or n == 0:
            print 'Not enough targets or agents for SMT solver'
            return 
        
        # Binary search through possible solutions        
        return self._binary_search(0, sum(self.w), 0)
        
    def _binary_search(self, TW_low, TW_high, rec_depth, rec_limit=200):
        """
        Search over the possible valid range of objective function values and
        return the max valid assignment.
        """        
#        print('range = [%d,%d]'%(TW_low,TW_high))  

        # Check is recursion limit is reached.        
#        print ('Current max. welfare = %d'%TW_low)
        if rec_depth >= rec_limit:
            print('Recursion limit reached before solution was found')
            return TW_low
        
        if abs(TW_high - TW_low) <= 10:
            self._generate_result_matrices()
            return TW_low
        
        TW_mid = (TW_low + TW_high) / 2
        
        # Since we're maximizing, first check the higher half of the range
        self._s.push()
        self._s.add(sum(self._W)>=TW_mid, self._TW==sum(self._W))
        if self._s.check() == z3.sat:
            self._generate_result_matrices()
#            new_sol = eval(self._s.model()[self._TW].as_decimal(12).replace('?',''))
            new_sol = self._s.model()[self._TW].as_long()
            self._s.pop()
            return self._binary_search(new_sol, TW_high, rec_depth+1)

        self._s.pop()
        self._s.push()
        self._s.add(sum(self._W)>TW_low, self._TW==sum(self._W))
        if self._s.check() == z3.sat:
            self._generate_result_matrices()
#            new_sol = eval(self._s.model()[self._TW].as_decimal(12).replace('?',''))
            new_sol = self._s.model()[self._TW].as_long()
            # This is a rounding error check condition
            self._s.pop()
            if abs(new_sol - TW_low) <= 10:                
                return TW_low
            else:
                return self._binary_search(new_sol, TW_mid, rec_depth+1)
        
        self._s.pop()
        return TW_low
    
    def _init_model(self):
        """
        Sets up all the decision variables and constraints except the objective
        max. constraints
        """
        # Z3 model solver
        self._s = z3.Solver() 
        self._s.set('timeout', taconst.Z3_TIMEOUT)
        
        # Decision variables
        self._x = [[z3.Int('x(%d,%d)'%(i,j)) for j in range(self.t)] for i in range(self.n)]
        self._W = [z3.Int('w(%d)'%(j)) for j in range(self.t)]
        self._TW = z3.Int('TW')
        
        # Result variables
        self._resM = [[0 for j in range(self.t)] for i in range(self.n)]
        self._resW = [0 for j in range(self.t)]
        
        # Reset the solver        
        self._s.reset()
        
        # Agent assignment constraints
        for i in range(self.n):
            for j in range(self.t):
#                self._s.add(Or(self._x[i][j]==1, self._x[i][j]==0))
                self._s.add(self._x[i][j]*self._x[i][j]==self._x[i][j]) # ensures x is 0 or 1
            self._s.add(sum(self._x[i]) <= 1)
            
        if len(self.cst) > 0:
            self._s.add(*[self._x[agent_id][trgt_id]==0 for (agent_id,trgt_id) in self.cst])
                
        # Target welfare constraints
        for j in range(self.t):
            self._s.add(z3.Or(self._W[j]==0., z3.And(sum([r[j] for r in self._x])>=self.k[j], self._W[j]==self.w[j]-sum([self._x[i][j] * self.d[i][j] for i in range(self.n)]))))
            
#        print self._s.assertions()

    def _set_ta_vars(self, n, t, k, w, cst, d):
        """
        Sets the optimization variables in object's memory
        """
        self.n   = n
        self.t   = t
        self.k   = [team_size for ((x,y), team_size) in k]
        self.w   = [int(utility * 100) for ((x,y), utility) in w]
        self.cst = cst
        self.d   = [[int(d[i][j] * 100) for j in range(t)] for i in range(n)]
        
#        print ('SMT Solver: Number of agents = %d'%self.n)
#        print ('SMT Solver: Number of targets = %d'%self.t)
#        print ('SMT Solver: Team size requirements')
#        print self.k
#        print ('SMT Solver: Target utilities')
#        print self.w
        
    def _generate_result_matrices(self):
        """
        Generates result matrix M and vector W for successful optimizations. See
        documentation of TASolver.solve() function for more details on these
        values.
        """
#        self._resM = [[eval(self._s.model()[self._x[i][j]].as_decimal(1)) for j in range(self.t)] for i in range(self.n)]
#        self._resW = [eval(self._s.model()[self._W[j]].as_decimal(12).replace('?','')) for j in range(self.t)]
        self._resM = [[self._s.model()[self._x[i][j]].as_long() for j in range(self.t)] for i in range(self.n)]
        self._resW = [self._s.model()[self._W[j]].as_long() / 100. for j in range(self.t)]
    
    
    