# Code written by Andy Huchala
# Computes a(n) for OEIS A261752
# (the minimum knights required to threaten all tiles
#    on an n x n chessboard)

# Requires installing Gurobi

# Select board size
n = 20

from gurobipy import *
m = Model("ip")

# initialize all variables of form x_j_i
for i in range(n):
    for j in range(n):
        if (i%n==0 and j%n ==0 and n>5):
            exec("x_" + str(j) + "_" + str(i)+" = m.addVar(lb=0,ub=0,vtype=GRB.BINARY, name=\"x_" + str(j) + "_" + str(i) + "\")")
        else:
            exec("x_" + str(j) + "_" + str(i)+" = m.addVar(lb=0,ub=1,vtype=GRB.BINARY, name=\"x_" + str(j) + "_" + str(i) + "\")")
        

# Set objective: minimize sum of x_i_j's

t = "x_0_0"

for j in range(n):
    for i in range(n):
        if i + j != 0:
            t += "+x_" + str(j) + "_" + str(i)
        
exec("obj = " + t)
m.setObjective(obj, GRB.MINIMIZE)


# specify constraints
for j in range(n):
    for i in range(n):
        # find all the locations from which (i,j) could be attacked, add each one to the constraint
        # for (i,j): (i,j) must be attacked
        
        s = "m.addLConstr("
        if (i-2 >= 0):
            if (j-1 >= 0):
                s += "x_" + str(j-1) + "_" + str(i-2) + "+"
            if (j+1 < n):
                s += "x_" + str(j+1) + "_" + str(i-2) + "+"
        if (i-1 >= 0):
            if (j-2 >= 0):
                s += "x_" + str(j-2) + "_" + str(i-1) + "+"
            if (j+2 < n):
                s += "x_" + str(j+2) + "_" + str(i-1) + "+"
        if (i+2 < n):
            if (j-1 >= 0):
                s += "x_" + str(j-1) + "_" + str(i+2) + "+"
            if (j+1 < n):
                s += "x_" + str(j+1) + "_" + str(i+2) + "+"
        if (i+1 < n):
            if (j-2 >= 0):
                s += "x_" + str(j-2) + "_" + str(i+1) + "+"
            if (j+2 < n):
                s += "x_" + str(j+2) + "_" + str(i+1) + "+"
        s = s[:-1]
        exec(s+ ">=1, \"" + "c_" + str(j) + "_" + str(i) + "\")")


m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())


# To plot, uncomment this
"""
printstr = ""
for v in m.getVars():
    printstr += str(int(v.x))
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (10,10)

# n = 10
s = printstr
# s = "0000000000001110000000100011100110001000000000001000000000100110001000001000111000111000000000000000"

M = np.zeros((n,n))


for i in range(n):
    for j in range(n):
        M[i][j] = int(s[j+n*i])

plt.matshow(M);

# plt.colorbar()
plt.axis('off')
plt.show()
"""