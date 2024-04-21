# Code written by Andy Huchala

# Computes a(n) for OEIS A072567
#   A variant of Zarankiewicz problem: maximal number of
#   1s in n X n 01-matrix with no four 1s forming a rectangle.

# Requires installing Gurobi

# Select board size (n>1)
n = 11

import math
from gurobipy import *
m = Model("ip")



# A[i,j] = x_i_j
for i in range(n):
    for j in range(n):
        exec("x_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j) + "\")")

# Set objective: maximize sum of x_i_j's
obj = LinExpr(0)

for i in range(n):
    for j in range(n):
        exec("obj.add(x_" + str(i) + "_" + str(j) +")")

m.setObjective(obj, GRB.MAXIMIZE)

# constraints -- iterate through corners of all rectangles, require not all be 1
#  __________________
# |i,j |   |   |i+a,j|
# |____|___|___|_____|
# |    |   |   |     |
# |____|___|___|_____|
# |    |   |   |     |
# |____|___|___|_____|
# |i   |   |   |i+a  |
# |j+b_|___|___|j+b__|

# i,j is top left vertex
for i in range(n-1):
    for j in range(n-1):
        for a in range(i,n):
            for b in range(j,n):
                l = LinExpr(0)
                exec("l.add(x_" + str(i) + "_" + str(j) + ")")
                exec("l.add(x_" + str(i+a) + "_" + str(j) + ")")
                exec("l.add(x_" + str(i) + "_" + str(j+b) + ")")
                exec("l.add(x_" + str(i+a) + "_" + str(j+b) + ")")
                exec("m.addConstr(l<=3)")

m.optimize()

# for v in m.getVars(): 
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())

# uncomment this to plot


# import numpy as np
# import matplotlib.pyplot as plt

# plt.rcParams["figure.figsize"] = (10,10)

# M = np.zeros((n,n))

# nonzero_vars = [a for a in m.getVars() if a.x > 0]
# for a in nonzero_vars:
#     foo,i,j = str(a).split("_")
#     i = int(i)
#     j = int(j.split(" ")[0])
#     M[i][j] = 1


# plt.matshow(M.transpose());

# # plt.colorbar()
# plt.axis('off')
# plt.show()