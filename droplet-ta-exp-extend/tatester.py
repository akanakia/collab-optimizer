# -*- coding: utf-8 -*-
from TASolver import TASolver


n = 6
t = 2
k = [((1,1),3),((0,0),2)]
w = [((1,1),3),((0,0),2)]
d = [[.1,.7],[.25,.25],[.5,.01],[.01,.5],[.6,.08],[.2,.3]]
solver = TASolver()
solver.solve(n,t,k,w,[],d)
(M, W) = solver.get_solution()
print M
print W