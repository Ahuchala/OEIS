# currently broken :(

# Code written by Andy Huchala
# Computes a(n) for OEIS A001197
# a(n) is the minimum number k_2(n) such that any 
# n X n matrix having that number of nonzero entries 
# has a 2 X 2 submatrix with only nonzero entries.

# Requires installing Gurobi



# Select matrix size
n = 9


from gurobipy import *
import math
m = Model("ip")



# initialize all variables of form x_i_j
for i in range(n):
	for j in range(n):
		exec(f"x_{i}_{j} = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_{i}_{j}\")")

# initialize all variables of form y_a_b_c_d
# which means 2x2 submatrix containing (a,b) and (c,d) is nonzero
for a in range(n):
	for b in range(n):
		for c in range(a):
			for d in range(b):
				exec(f"y_{a}_{b}_{c}_{d} = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"y_{a}_{b}_{c}_{d}\")")

            
# Set objective: minimize sum of x_i_j


obj = LinExpr(0)
for i in range(n):
	for j in range(n):
		exec(f"obj.add(x_{i}_{j})")


m.setObjective(obj, GRB.MINIMIZE)


# specify constraints
# avoid zero submatrix with top left coordinate (a,b) and bottom right (c,d)
# can assume a > c and b >d

for a in range(n):
	for b in range(n):
		for c in range(a):
			for d in range(b):
				constraint = LinExpr(0)
				exec(f"constraint.add(x_{a}_{b})")
				exec(f"constraint.add(x_{c}_{b})")
				exec(f"constraint.add(x_{a}_{d})")
				exec(f"constraint.add(x_{c}_{d})")
				exec(f"m.addGenConstrIndicator(y_{a}_{b}_{c}_{d},True,constraint>=4)")	



constraint = LinExpr(0)
for a in range(n):
	for b in range(n):
		for c in range(a):
			for d in range(b):
				exec(f"constraint.add(y_{a}_{b}_{c}_{d})")
exec(f"m.addLConstr(constraint>=1)")



m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())


