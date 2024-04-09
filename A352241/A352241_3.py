# bfile code

# Code written by Andy Huchala
# Computes a(n) for OEIS A352241
# (the maximal number of nonattacking
 # black-square queens on an n x n board)

# possible g.f. (1 + z^3 + z^4 + z^6)/(1 - z - z^5 + z^6)

# Requires installing Gurobi

# Select board size (n>1)
from gurobipy import *
m = Model("ip")

import numpy as np
import matplotlib.pyplot as plt

ls = [0]
ls += [ 1, 1, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 9, 10, 11, 12, 13, 13, 14, 15, 16, 17, 17, 18, 19, 20, 21, 21, 22, 23, 24, 25, 25, 26, 27, 28, 29, 29, 30, 31, 32, 33, 33, 34, 35, 36, 37, 37, 38, 39, 40, 40, 41, 42, 43, 44, 44, 45, 46, 47]
for _ in range(300):
    ls.append(0)
# Select board width (n>1)
for n in range(61,300):


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