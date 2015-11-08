# -*- coding: utf-8 -*-
import z3

Z3_TIMEOUT = 1000 * 10 # 10 seconds, I hope
RECURSION_LIMIT = 200

class StaticTASolver:
    def get_solution(self):
        return (self._resM, self._resW)
        
    def solve(self, n = 0, t = 0, k = [], w = [], d = [], x=1):
        """
        Solves the Target Assignemt problem for the given input argunemts:
        n   = Number of agents.
        t   = Number of targets.
        k   = List of minimum team size requirements per target. 
        w   = List of payoffs/welfare per target for a successful assignment.
        d   = The |n| x |t| distance-payoff matrix. The values d_{ij} in this 
              matrix should contain the normalized penalty for assigning agent
              i to target j. All values in this matrix should be non-negative.
              The column order of this matrix (i.e. order of targets) needs to
              be consistent with the ordering of lists k and w.
        x   = An integer value used to halt the solver when a solution is
              considered close enough to optimal. The value is used in
              the conditional: stop if abs(new_sol - old_sol) <= x.
              
              
        This function fills a 0/1 |n| x |t| matrix-M indicating agent-target
        assignments as well a vector-W of size t indicating the welfare received
        for each successfully assigned target. if no valid assignments are found
        then (M, W) = (None, None)
        """        
        # Setup initial constraints & add a backtracking point
        self._set_ta_vars(n, t, k, w, d, x)
        self._init_model()

        # If there are no targets return immediately        
        if t == 0 or n == 0:
            print 'Not enough targets or agents for SMT solver'
            return 
        
        # Binary search through possible solutions      
        res = self._binary_search(0, sum(self.w), 0)
        self._s.reset()
        z3.reset_params()
        return res
        
    def _binary_search(self, TW_low, TW_high, rec_depth, rec_limit=RECURSION_LIMIT):
        """
        Search over the possible valid range of objective function values and
        return the max valid assignment.
        """        
        # Check is recursion limit is reached.        
        if rec_depth >= rec_limit:
            print('Solver recursion limit reached. Dropping this solution')
            return TW_low
        
        if abs(TW_high - TW_low) <= self.x:
            self._generate_result_matrices()
            self.solution_found = True
            return TW_low
        
        TW_mid = (TW_low + TW_high) / 2
        
        # Since we're maximizing, first check the higher half of the range
        try:
            self._s.push()
            self._s.add(sum(self._W)>=TW_mid, self._TW==sum(self._W))
            res = self._s.check()
        # There are at least 2 unique exceptions I've seen thrown by the solver.
        # I'm just going to catch any exception for now.
        except: 
            print('Hit a Z3 exception. Dropping this solution.')
            return TW_low
            
        if res == z3.sat:
            self._generate_result_matrices()
            new_sol = self._s.model()[self._TW].as_long()
            self._s.pop()
            return self._binary_search(new_sol, TW_high, rec_depth+1)
        if res == z3.unknown:
            print('Solver timed out. Dropping this solution.')
            return TW_low
            
        self._s.pop()
        try:
            self._s.push()
            self._s.add(sum(self._W)>TW_low, self._TW==sum(self._W))
            res = self._s.check()
        # There are at least 2 unique exceptions I've seen thrown by the solver.
        # I'm just going to catch any exception for now.        
        except:
            print('Hit a Z3 exception. Dropping this solution.')
            return TW_low
            
        if res == z3.sat:
            self._generate_result_matrices()
            new_sol = self._s.model()[self._TW].as_long()
            
            # This is a rounding error check condition
            self._s.pop()
            if abs(new_sol - TW_low) <= self.x:
                self.solution_found = True
                return TW_low
            else:
                return self._binary_search(new_sol, TW_mid, rec_depth+1)
        if res == z3.unknown:
            print('Solver timed out. Dropping this solution.')
            return TW_low
        
        self._s.pop()
        return TW_low
    
    def _init_model(self):
        """
        Sets up all the decision variables and constraints except the objective
        max. constraints
        """
        # Z3 model solver
        z3.reset_params()
        self._s = z3.Solver() 
        self._s.reset()
        self._s.set('timeout', Z3_TIMEOUT)
        self.solution_found = False
        
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
                self._s.add(self._x[i][j]*self._x[i][j]==self._x[i][j]) # ensures x is 0 or 1
            self._s.add(sum(self._x[i]) <= 1)
        
        # Target welfare constraints
        for j in range(self.t):
            self._s.add(z3.Or(self._W[j]==0., z3.And(sum([r[j] for r in self._x])>=self.k[j], self._W[j]==self.w[j]-sum([self._x[i][j] * self.d[i][j] for i in range(self.n)]))))

    def _set_ta_vars(self, n, t, k, w, d, x):
        """
        Sets the optimization variables in object's memory
        """
        self.n = n
        self.t = t
        self.k = k
        self.w = w
        self.d = d
        self.x = x
        
    def _generate_result_matrices(self):
        """
        Generates result matrix M and vector W for successful optimizations. See
        documentation of TASolver.solve() function for more details on these
        values.
        """
        self._resM = [[self._s.model()[self._x[i][j]].as_long() for j in range(self.t)] for i in range(self.n)]
        self._resW = [self._s.model()[self._W[j]].as_long() / 100. for j in range(self.t)]
    
    
    