# Code written by Andy Huchala
# Computes a(n) for OEIS A250000 
# (the maximal peaceable queen armies)

# Requires installing Gurobi

# Select board size (n>1)
n = 8


import math
from gurobipy import *
m = Model("ip")

# white queens x, black queens y
# initialize all variables of form x_j_i, y_j_i

for i in range(n):
    for j in range(n):
        exec("x_" + str(j) + "_" + str(i)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(j) + "_" + str(i) + "\")")
        exec("y_" + str(j) + "_" + str(i)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"y_" + str(j) + "_" + str(i) + "\")")

# Set objective: minimize sum of x_i_j's

t = "x_0_0"

for j in range(n):
    for i in range(n):
        if i + j != 0:
            t += "+x_" + str(j) + "_" + str(i)
        
exec("obj = " + t)
m.setObjective(obj, GRB.MAXIMIZE)


# specify constraints

# at least as many black queens
s = "y_0_0"
for j in range(n):
    for i in range(n):
        if i + j != 0:
            s += "+y_" + str(j) + "_" + str(i)
exec("m.addLConstr(" + s + ">= " + t + ")")


for j in range(n):
    for i in range(n):
        # find all the locations from which (i,j) could be attacked, add each one to the constraint
        # for (i,j): (i,j) must may be attacked by one color xor occupied by another
        
        p_x = "x_" + str(j) + "_" + str(i)
        p_y = "y_" + str(j) + "_" + str(i)

        exec("m.addLConstr(" + p_x + " + " + p_y + " <= 1)")
        for k in range(n):
            if k != j:
                s_x = "x_" + str(k) + "_" + str(i) 
                s_y = "y_" + str(k) + "_" + str(i)
                exec("m.addLConstr(" + p_x + " + " + s_y + "<= 1)")
                exec("m.addLConstr(" + s_x + " + " + p_y + "<= 1)")
            if k != i:
                s_x = "x_" + str(j) + "_" + str(k) 
                s_y = "y_" + str(j) + "_" + str(k)
                exec("m.addLConstr(" + p_x + " + " + s_y + "<= 1)")
                exec("m.addLConstr(" + s_x + " + " + p_y + "<= 1)")
            if i-j+k>=0 and i-j+k<n:
                if k != j or (i-j+k) != i: 
                    s_x = "x_" + str(k) + "_" + str(i-j+k) 
                    s_y = "y_" + str(k) + "_" + str(i-j+k)
                    exec("m.addLConstr(" + p_x + " + " + s_y + "<= 1)")
                    exec("m.addLConstr(" + s_x + " + " + p_y + "<= 1)")
            if 2*i-(i-j+k)>=0 and 2*i-(i-j+k)<n:
                if k != j or 2*i-(i-j+k) != i:
                    s_x = "x_" + str(k) + "_" + str(2*i-(i-j+k)) 
                    s_y = "y_" + str(k) + "_" + str(2*i-(i-j+k))
                    exec("m.addLConstr(" + p_x + " + " + s_y + "<= 1)")
                    exec("m.addLConstr(" + s_x + " + " + p_y + "<= 1)")



m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())

# uncomment this to plot
# xstr = ""
# ystr = ""
# for v in m.getVars():
#     if 'x' in str(v):
#         xstr += str(int(v.x+.01))
#     elif 'y' in str(v):
#         ystr += str(int(v.x+.01))
# import numpy as np
# import matplotlib.pyplot as plt

# plt.rcParams["figure.figsize"] = (10,10)

# # n = 10
# # s = printstr
# # s = "0000000000001110000000100011100110001000000000001000000000100110001000001000111000111000000000000000"

# M = np.zeros((n,n))


# for i in range(n):
#     for j in range(n):
#         M[i][j] = int(xstr[j+n*i])-int(ystr[j+n*i])

# plt.matshow(M);

# # plt.colorbar()
# plt.axis('off')
# plt.show()