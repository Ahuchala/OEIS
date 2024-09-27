# Code written by Andy Huchala
# Computes a(n) for OEIS A004035 
# The coding-theoretic function A(n,4,5).

# (equivalently, the size of maximal binary code of length n, covering radius 4,
#  and constaint weight 5.)
# Requires installing Gurobi


n = 4

from gurobipy import *
import math
m = Model("ip")

d = 4 #distance
w = 5 #weight, set to -1 to ignore

		
# initialize all variables of form x_i
for i in range(2**n):
	
	exec(f"x_{i} = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_{i}\")")


			
# Set objective: minimize sum of x_i's

vertex_set = set()

obj = LinExpr(0)

for i in range(2**n):
	if w<0 or sum(map(int,format(i,'b')))==w: #check weight
		vertex_set.add(i)
		exec(f"obj.add(x_{i})")

m.setObjective(obj, GRB.MAXIMIZE)

# specify constraints
for i in vertex_set:

	
	# find all nodes within d of i

	for j in vertex_set:

		# check if at most d bits are different
		constraint = LinExpr(0)
		if i!=j and sum(map(int,format(i^j,'b')))<d:

			exec(f"constraint.add(x_{j})")

		exec(f"m.addGenConstrIndicator(x_{i},True,constraint==0)")

m.optimize()

# for v in m.getVars():
#	 print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())
