# duplicate version meant for practice tuning

# Code written by Andy Huchala
# Computes a(n) for OEIS A352241
# (the maximal number of nonattacking
 # black-square queens on an n x n board)

# possible g.f. (1 + z^3 + z^4 + z^6)/(1 - z - z^5 + z^6)

# Requires installing Gurobi

# Select board size (n>1)
n = 51

from gurobipy import *
m = Model("ip")

# these were some good parameters found for n = 50

        # BranchDir 1
        # Heuristics 0
        # VarBranch 1
        # Cuts 0
        # PreDepRow 1
# m.setParam("Method", 0)
# m.setParam("SimplexPricing", 0)
# m.setParam("BranchDir", 1)
# m.setParam("DegenMoves", 9)
# m.setParam("Heuristics", 0)
# m.setParam("Varbranch", 1)
# m.setParam("Cuts", 0)
# m.setParam("PrePasses", 5)
# m.setParam("Presolve", 2)
# m.setParam("PreDepRow", 1)

# initialize all variables of form x_j_i
for i in range(n):
    for j in range(n):
        if (i + j) % 2 == 0:
            exec("x_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j) + "\")")
        

# Set objective: maximize sum of x_i_j's

obj = LinExpr(0)

for i in range(n):
    for j in range(n):
        if (i + j) % 2 == 0:
            exec("obj.add(x_" + str(i) + "_" + str(j) +")")

m.setObjective(obj, GRB.MAXIMIZE)


# specify constraints

# all row, column, and diagonal sums must be <= 1

# look, the python code isn't pretty, but the result is efficient

# columns
for a in range(n):
    s = LinExpr(0)
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                if a == i:
                    exec("s.add(x_" + str(i) + "_" + str(j) +")")
    m.addLConstr(s<=1)

# rows
for b in range(n):
    s = LinExpr(0)
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                if b == j:
                    exec("s.add(x_" + str(i) + "_" + str(j) +")")
    m.addLConstr(s<=1)

# \\ diagonal
for k in range(-n,n):
    s = LinExpr(0)
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                if i - j == k:
                    exec("s.add(x_" + str(i) + "_" + str(j) +")")
    m.addLConstr(s<=1)

# // diagonal
for k in range(2*n):
    s = LinExpr(0)
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                if i + j == k:
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