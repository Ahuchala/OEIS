# Code written by Andy Huchala
# Computes a(n) for OEIS A287864 
# (the maximal number of nonattacking
 # queens on a quarter chessboard

# Requires installing Gurobi
from gurobipy import *
m = Model("ip")

import numpy as np
import matplotlib.pyplot as plt

ls = [0]
for _ in range(300):
    ls.append(0)
# Select board width (n>1)
for n in range(1,300):


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

    ls[n] = int(0.5 + obj.getValue())
    print(n,ls[n])
    print(ls)

    plt.rcParams["figure.figsize"] = (10,10)

    M = np.zeros((n,(n+1)//2))

    nonzero_vars = [a for a in m.getVars() if a.x > 0]
    for a in nonzero_vars:
        foo,i,j = str(a).split("_")
        i = int(i)
        j = int(j.split(" ")[0])
        M[i][j] = 1
    # for j in range(n):
    #     for i in range(j,2*n-j-1):
    #         if m.getVar("x_" + str(i) + "_" + str(j)).x > 0:
    #             print(i,j)
    #         else:
    #             print(m.getVarByName("x_" + str(i) + "_" + str(j)))
    #         M[i][j] = int(0.1+m.getVarByName("x_" + str(i) + "_" + str(j)).x)+1


    plt.matshow(M.transpose());

    # plt.colorbar()
    plt.axis('off')
    exec("plt.savefig('C:/Users/Ahuch/Documents/GitHub/OEIS/Images/A287864_" + str(n) + ".png')")
    plt.show()