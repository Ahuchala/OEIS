# bfile code

# Code written by Andy Huchala
# Computes a(n) for OEIS 352426
# (the maximal number of nonattacking
 # white-square queens on an n x n board)

# Requires installing Gurobi

# Select board size (n>1)
from gurobipy import *
m = Model("ip")

import numpy as np
import matplotlib.pyplot as plt

ls = [0]
ls += [0, 1, 1, 2, 4, 4, 4, 5, 6, 7, 8, 9, 10, 10, 11, 12, 13, 13, 14, 15, 16, 17, 18, 18, 19, 20, 21, 21, 22, 23, 24, 25, 26, 26, 27, 28, 29, 29, 30, 31, 32, 33, 33, 34, 35, 36, 36, 37, 38, 39, 40, 40, 41, 42, 43, 44, 44, 45, 46, 47, 48, 48, 49, 50, 51, 51, 52, 53, 54, 55, 55, 56, 57, 58, 59, 59, 60, 61, 62, 63, 63, 64, 65]
for _ in range(300):
    ls.append(0)
# Select board width (n>1)
for n in range(82+1,82+300):


    # initialize all variables of form x_j_i
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 1:
                exec("x_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j) + "\")")


    # Set objective: maximize sum of x_i_j's

    obj = LinExpr(0)

    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 1:
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
                if (i + j) % 2 == 1:
                    if a == i:
                        exec("s.add(x_" + str(i) + "_" + str(j) +")")
        m.addLConstr(s<=1)

    # rows
    for b in range(n):
        s = LinExpr(0)
        for i in range(n):
            for j in range(n):
                if (i + j) % 2 == 1:
                    if b == j:
                        exec("s.add(x_" + str(i) + "_" + str(j) +")")
        m.addLConstr(s<=1)

    # \\ diagonal
    for k in range(-n,n):
        s = LinExpr(0)
        for i in range(n):
            for j in range(n):
                if (i + j) % 2 == 1:
                    if i - j == k:
                        exec("s.add(x_" + str(i) + "_" + str(j) +")")
        m.addLConstr(s<=1)

    # // diagonal
    for k in range(2*n):
        s = LinExpr(0)
        for i in range(n):
            for j in range(n):
                if (i + j) % 2 == 1:
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