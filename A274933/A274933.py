# Code written by Andy Huchala
# Computes a(n) for OEIS A274933 
# (the maximal number of nonattacking
 # queens on a quarter chessboard containing 
 # n^2 squares)

# Requires installing Gurobi

# Select board height (n>1)
n = 10


from gurobipy import *
m = Model("ip")

# initialize all variables of form x_j_i
for j in range(n):
    for i in range(j,2*n-j-1):
        exec("x_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j) + "\")")
        

# Set objective: minimize sum of x_i_j's

obj = LinExpr(0)

for j in range(n):
    for i in range(j,2*n-j-1):
         exec("obj.add(x_" + str(i) + "_" + str(j) +")")

m.setObjective(obj, GRB.MAXIMIZE)


# specify constraints
for j in range(n):
    for i in range(j,2*n-j-1):

        # find all the locations from which (i,j) could be attacked, add each one to the constraint
        
        exec("s = LinExpr(x_" + str(i) + "_" + str(j) +")")
        for k in range(2*n):
            if k != j and k < n:
                a,b = i,k
                if a >= b and a < 2*n - b-1:
                    exec("s.add(x_" + str(a) + "_" + str(b) +")")
        m.addLConstr(s<=1)

        exec("s = LinExpr(x_" + str(i) + "_" + str(j) +")")

        for k in range(2*n):
            if k != i:
                a,b = k,j
                if a >= b and a < 2*n - b-1:
                    exec("s.add(x_" + str(a) + "_" + str(b) +")")
        m.addLConstr(s<=1)

        exec("s = LinExpr(x_" + str(i) + "_" + str(j) +")")
        for k in range(2*n):
            if i-j+k>=0 and i-j+k< 2*n and k < n:
                if k != j or (i-j+k) != i: 
                    a,b = i-j+k,k
                    if a >= b and a < 2*n - b-1:
                        exec("s.add(x_" + str(a) + "_" + str(b) +")")
        m.addLConstr(s<=1)

        exec("s = LinExpr(x_" + str(i) + "_" + str(j) +")")
        for k in range(2*n):
            if 2*i-(i-j+k)>=0 and 2*i-(i-j+k)<2*n and k < n:
                if k != j or 2*i-(i-j+k) != i:
                    a,b = 2*i-(i-j+k), k
                    if a >= b and a < 2*n - b-1:
                        exec("s.add(x_" + str(a) + "_" + str(b) +")")
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