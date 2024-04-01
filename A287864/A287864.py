# Code written by Andy Huchala
# Computes a(n) for OEIS A287864 
# (the maximal number of nonattacking
 # queens on a quarter chessboard

# Requires installing Gurobi

# Select board width (n>1)
n = 10


from gurobipy import *
m = Model("ip")

# initialize all variables of form x_j_i
for j in range((n+1)//2):
    for i in range(j,n-j):
        exec("x_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j) + "\")")
        

# Set objective: minimize sum of x_i_j's

obj = LinExpr(0)

for j in range((n+1)//2):
    for i in range(j,n-j):
         exec("obj.add(x_" + str(i) + "_" + str(j) +")")

m.setObjective(obj, GRB.MAXIMIZE)


# specify constraints

# all row, column, and diagonal sums must be <= 1

# look, the python code isn't pretty, but the result is efficient

# columns
for a in range(n):
    s = LinExpr(0)
    for j in range((n+1)//2):
        for i in range(j,n-j):
            if a == i:
                exec("s.add(x_" + str(i) + "_" + str(j) +")")
    m.addLConstr(s<=1)

# rows
for b in range(n):
    s = LinExpr(0)
    for j in range((n+1)//2):
        for i in range(j,n-j):
            if b == j:
                exec("s.add(x_" + str(i) + "_" + str(j) +")")
    m.addLConstr(s<=1)

# \\ diagonal
for k in range(n):
    s = LinExpr(0)
    for j in range((n+1)//2):
        for i in range(j,n-j):
            if i - j == k:
                exec("s.add(x_" + str(i) + "_" + str(j) +")")
    m.addLConstr(s<=1)

# // diagonal
for k in range(n):
    s = LinExpr(0)
    for j in range((n+1)//2):
        for i in range(j,n-j):
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

# M = np.zeros((2*n-1,n))


# for i in range(2*n-1):
#     for j in range(n):
#         if i >= j and i < 2*n-j-1:
#             M[i][j] = int(m.getVarByName("x_" + str(i) + "_" + str(j)).x)


# plt.matshow(M.transpose());

# # plt.colorbar()
# plt.axis('off')
# plt.show