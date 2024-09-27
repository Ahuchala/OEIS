# Code written by Andy Huchala
# Computes a(n) for OEIS A070214 

# Maximal number of occupied cells in all monotonic matrices of order n.

# Requires installing Gurobi


n = 3

from gurobipy import *
import math
m = Model("ip")

# From Rob Pratt: The problem can be formulated as a maximum independent set problem in a graph with n^3 nodes (i, j, k) in {1, 2, ..., n}^3. If node (i, j, k) appears in the solution, the interpretation is that cell (i, j) should contain k. The arcs, which indicate conflicting choices, are as follows:
# Arc joining (i1, j1, k1) and (i2, j2, k2) if:
# [rows increasing] i1 = i2 and ((j1 < j2 and k1 >= k2) or (j1 > j2 and k1 <= k2)).
# [columns decreasing] j1 = j2 and ((i1 < i2 and k1 <= k2) or (i1 > i2 and k1 >= k2)).
# [one color per cell] i1 = i2 and j1 = j2 and k1 <> k2.
# [positive slope] k1 = k2 and i1 <> i2 and (j2 - j1) / (i2 - i1) > 0.


# initialize all variables of form x_i_j_k
for i in range(n):
    for j in range(n):
        for k in range(n):
            exec(f"x_{i}_{j}_{k} = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = \"x_{i}_{j}_{k}\")")

            
# Set objective: maximize sum of x_i_j_k's



obj = LinExpr(0)
for i in range(n):
    for j in range(n):
        for k in range(n):
            exec(f"obj.add(x_{i}_{j}_{k})")


m.setObjective(obj, GRB.MAXIMIZE)


# specify constraints

# Arc joining (i1, j1, k1) and (i2, j2, k2) if:
# [rows increasing] i1 = i2 and ((j1 < j2 and k1 >= k2) or (j1 > j2 and k1 <= k2)).
# [columns decreasing] j1 = j2 and ((i1 < i2 and k1 <= k2) or (i1 > i2 and k1 >= k2)).
# [one color per cell] i1 = i2 and j1 = j2 and k1 <> k2.
# [positive slope] k1 = k2 and i1 <> i2 and (j2 - j1) / (i2 - i1) > 0.

for i1 in range(n):
    for j1 in range(n):
        for k1 in range(n):
            for i2 in range(n):
                for j2 in range(n):
                    for k2 in range(n):
                        if i1 == i2 and ((j1 < j2 and k1 >= k2) or (j1 > j2 and k1 <= k2)):
                            constraint = LinExpr(0)
                            exec(f"constraint.add(x_{i1}_{j1}_{k1})")
                            exec(f"constraint.add(x_{i2}_{j2}_{k2})")
                            exec(f"m.addLConstr(constraint <= 1)")
                        if j1 == j2 and ((i1 < i2 and k1 <= k2) or (i1 > i2 and k1 >= k2)):
                            constraint = LinExpr(0)
                            exec(f"constraint.add(x_{i1}_{j1}_{k1})")
                            exec(f"constraint.add(x_{i2}_{j2}_{k2})")
                            exec(f"m.addLConstr(constraint <= 1)")
                        if i1 == i2 and j1 == j2 and k1 != k2:
                            constraint = LinExpr(0)
                            exec(f"constraint.add(x_{i1}_{j1}_{k1})")
                            exec(f"constraint.add(x_{i2}_{j2}_{k2})")
                            exec(f"m.addLConstr(constraint <= 1)")
                        if k1 == k2 and i1 != i2 and (j2 - j1) / (i2 - i1) > 0:
                            constraint = LinExpr(0)
                            exec(f"constraint.add(x_{i1}_{j1}_{k1})")
                            exec(f"constraint.add(x_{i2}_{j2}_{k2})")
                            exec(f"m.addLConstr(constraint <= 1)")


m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())

# to print
M = [[" " for _ in range(n)] for _ in range(n)]
for v in m.getVars():
    if v.x == 1:
        foo, i,j,k = v.varName.split("_")
    M[int(i)][int(j)] = int(k)
import numpy as np
np.array(M)