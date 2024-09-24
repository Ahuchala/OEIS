# Code written by Andy Huchala
# Computes a(n) for OEIS A065825
# Smallest k such that n numbers may be picked in 
# {1,...,k} with no three terms in arithmetic progression.

# Requires installing Gurobi



# Select number of terms
n = 9

# Make a guess for an upper bound, and remember to throw an error if it doesn't work


k = int(0.64*(n**1.534)+7.9)

from gurobipy import *
import math
m = Model("ip")



# initialize all variables of form x_i
for i in range(1,k+1):
    exec(f"x_{i} = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_{i}\")")

# initialize auxiliary variables of form y_i, and x_j = 0 if y_i = 1 for j >= i
for i in range(1,k+1):
    exec(f"y_{i} = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"y_{i}\")")

            
# Set objective: maximize sum of y_i's, equivalently minimize k - sum(y_i)


obj = LinExpr(k)
for i in range(1,k+1):
    exec(f"obj.add(-y_{i})")


m.setObjective(obj, GRB.MINIMIZE)


# specify constraints
# avoid 3-term arithmetic progressions, ie a, a+b, a+2b

for a in range(1,k+1):
	for b in range(1,k+1):
		if a + 2*b <= k:
			constraint = LinExpr(0)
			exec(f"constraint.add(x_{a})")
			exec(f"constraint.add(x_{a+b})")
			exec(f"constraint.add(x_{a+2*b})")
			exec(f"m.addLConstr(constraint<=2)")			

# pick exactly n numbers
constraint = LinExpr(0)
for i in range(1,k+1):
	exec(f"constraint.add(x_{i})")
exec(f"m.addLConstr(constraint=={n})")	

# require x_j = 0 if y_i = 1 for j >= i
for i in range(1,k+1):
	
	for j in range(i,k+1):
		constraint = LinExpr(0)
		exec(f"constraint.add(y_{i})")
		exec(f"constraint.add(x_{j})")
		exec(f"m.addLConstr(constraint<=1)")			


m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())
print([int(v.varName[2:]) for v in m.getVars()[:k] if v.x > 0.1])


