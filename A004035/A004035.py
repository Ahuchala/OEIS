# Code written by Andy Huchala
# Computes a(n) for OEIS A004035 
# The coding-theoretic function A(n,4,5).

# (equivalently, the size of maximal binary code of length n, covering radius 4,
#  and constant weight 5.)
# Requires installing Gurobi



n = 8

from gurobipy import *
import math

import sympy
from sympy.utilities.iterables import multiset_permutations

m = Model("ip")

d = 4 #distance
w = 5 #weight, set to -1 to ignore

# from https://stackoverflow.com/questions/12461361/bits-list-to-integer-in-python
# in: [0,1,1]
# out: 3
def arr_to_int(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out		

vertex_set = set()
if w > 0:
	# equivalent to
	# if sum(map(int,format(i,'b')))==w: #check weight

	w_vector = w * [1] + (n-w) * [0]
	w_vector_perms = multiset_permutations(w_vector)
	for i in w_vector_perms:
		vertex_set.add(arr_to_int(i))
else:
	for i in range(2**n):
		vertex_set.add(i)


# initialize all variables of form x_i with i an int
for i in vertex_set:	
	exec(f"x_{i} = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_{i}\")")


			
# Set objective: minimize sum of x_i's



obj = LinExpr(0)

for i in vertex_set:
	exec(f"obj.add(x_{i})")

m.setObjective(obj, GRB.MAXIMIZE)



# iterate through all k bit swaps for k = 1...d, or all points in the radius d sphere
neighbor_set = set()

for k in range(1,d):
	# create n-k 0's and k 1's
	k_vector = k * [1] + (n-k) * [0]
	k_vector_perms = multiset_permutations(k_vector)
	for pt in k_vector_perms:
		neighbor_set.add(arr_to_int(pt))



# specify constraints
for i in vertex_set:


	
	constraint = LinExpr(0)
	for pt in neighbor_set:
		if pt^i in vertex_set:
			exec(f"constraint.add(x_{pt^i})")

	exec(f"m.addGenConstrIndicator(x_{i},True,constraint==0)")

m.optimize()

# for v in m.getVars():
#	 print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())



