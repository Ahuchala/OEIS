# Code written by Andy Huchala
# Computes a(n) for OEIS A352241
# (the maximal number of nonattacking
 # black-square queens on an n x n board)


# Requires installing Gurobi

# Select board size (n>1)
n = 19

from gurobipy import *
m = Model("ip")

# initialize all variables of form x_j_i
for i in range(n):
    for j in range(n):
        exec("x_" + str(j) + "_" + str(i)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(j) + "_" + str(i) + "\")")
        

# Set objective: minimize sum of x_i_j's

t = "x_0_0"

for j in range(n):
    for i in range(n):
        if i + j != 0:
            t += "+x_" + str(j) + "_" + str(i)
        
exec("obj = " + t)
m.setObjective(obj, GRB.MAXIMIZE)


# specify constraints
for j in range(n):
    for i in range(n):
        # black tile
        if (i+j)%2 == 0:
            # find all the locations from which (i,j) could be attacked, add each one to the constraint
            # for (i,j): (i,j) must be attacked or occupied
            
            s = "m.addGenConstrIndicator("
            s += "x_" + str(j) + "_" + str(i) + ",1,"
            for k in range(n):
                if k != j:
                    s += "x_" + str(k) + "_" + str(i) + "+"
                if k != i:
                    s += "x_" + str(j) + "_" + str(k) + "+"
                if i-j+k>=0 and i-j+k<n:
                    if k != j or (i-j+k) != i: 
                        s += "x_" + str(k) + "_" + str(i-j+k) + "+"
                if 2*i-(i-j+k)>=0 and 2*i-(i-j+k)<n:
                    if k != j or 2*i-(i-j+k) != i:
                        s += "x_" + str(k) + "_" + str(2*i-(i-j+k)) + "+"

            s = s[:-1]

            exec(s+ "==0)")
        else:
            exec("m.addLConstr(x_" + str(j) + "_" + str(i) + "==0)")



m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())

# uncomment this to plot
# printstr = ""
# mgetVars = [v for v in m.getVars() if 'x_' in str(v)]
# for v in mgetVars:
#     printstr += str(int(v.x))
# import numpy as np
# import matplotlib.pyplot as plt

# plt.rcParams["figure.figsize"] = (10,10)

# # n = 10
# s = printstr
# # s = "0000000000001110000000100011100110001000000000001000000000100110001000001000111000111000000000000000"

# M = np.zeros((n,n))


# for i in range(n):
#     for j in range(n):
#         # alternate checkerboard coloring
#         # if int(s[j+n*i]) == 1:
#         #     M[i][j] = 0.5
#         # if int(s[j+n*i]) == 0:
#         #     M[i][j] = -1-((1+i + j) % 2)/5
#         if int(s[j+n*i]) == 1:
#             M[i][j] = 1
#         if int(s[j+n*i]) == 0:
#             M[i][j] = 0

# plt.matshow(M);

# # plt.colorbar()
# plt.axis('off')
# plt.show()