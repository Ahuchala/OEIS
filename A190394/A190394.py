# Code written by Andy Huchala
# Computes a(n) for OEIS A190394
# (the maximal number of nonattacking nightriders
#  one an n x n board)

# nightriders can move any distance in a direction
# specified by a knight


# Requires installing Gurobi

# Select board size (n>1)
n = 19

from gurobipy import *
m = Model("ip")

# initialize all variables of form x_j_i
for i in range(n):
    for j in range(n):
        exec("x_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j) + "\")")
        

# Set objective: maximize sum of x_i_j's

obj = LinExpr(0)

for i in range(n):
    for j in range(n):
        exec("obj.add(x_" + str(i) + "_" + str(j) +")")

m.setObjective(obj, GRB.MAXIMIZE)


# specify constraints

# an efficient way to enforce constraints is to sum along directions of knight movements
# 00 21 42 

for (a,b) in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
    for k in range(-3*n,3*n):
        s = LinExpr(0)
        for i in range(n):
            for j in range(n):
                if a*i + b*j == k:
                    exec("s.add(x_" + str(i) + "_" + str(j) +")")
        m.addLConstr(s<=1)


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
# # for j in range(n):
# #     for i in range(j,2*n-j-1):
# #         if m.getVar("x_" + str(i) + "_" + str(j)).x > 0:
# #             print(i,j)
# #         else:
# #             print(m.getVarByName("x_" + str(i) + "_" + str(j)))
# #         M[i][j] = int(0.1+m.getVarByName("x_" + str(i) + "_" + str(j)).x)+1


# plt.matshow(M.transpose());

# # plt.colorbar()
# plt.axis('off')
# plt.show()