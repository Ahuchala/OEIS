# makes b-file

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
# ls += [1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 28, 29, 29, 30, 30, 31, 31, 32, 32, 33, 33, 34, 34, 35, 35, 35, 36, 36, 37, 37, 38, 38, 39, 39, 40, 40, 41, 41, 42, 42, 42, 43, 43, 44, 44, 45, 45, 46, 46, 47, 47, 48, 48, 49, 49, 50, 50, 50, 51, 51, 52, 52, 53, 53, 54, 54, 55, 55, 56, 56, 57, 57, 57, 58, 58, 59, 59, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 64, 65, 65, 66, 66, 67, 67, 68, 68, 69, 69, 70, 70, 71, 71, 71, 72, 72, 73, 73, 74, 74, 75, 75, 76, 76, 77, 77, 78, 78, 78, 79, 79, 80, 80, 81, 81, 82, 82, 83, 83, 84, 84, 85, 85, 85, 86, 86, 87, 87, 88, 88, 89, 89, 90, 90, 91, 91, 92, 92, 92, 93, 93, 94, 94, 95, 95, 96, 96, 97, 97, 98, 98, 99, 99]
for _ in range(500):
    ls.append(0)
# Select board width (n>1)
for n in range(1,500):


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

    # plt.rcParams["figure.figsize"] = (10,10)

    # M = np.zeros((n,(n+1)//2))

    # nonzero_vars = [a for a in m.getVars() if a.x > 0]
    # for a in nonzero_vars:
    #     foo,i,j = str(a).split("_")
    #     i = int(i)
    #     j = int(j.split(" ")[0])
    #     M[i][j] = 1
    # for j in range(n):
    #     for i in range(j,2*n-j-1):
    #         if m.getVar("x_" + str(i) + "_" + str(j)).x > 0:
    #             print(i,j)
    #         else:
    #             print(m.getVarByName("x_" + str(i) + "_" + str(j)))
    #         M[i][j] = int(0.1+m.getVarByName("x_" + str(i) + "_" + str(j)).x)+1


    # plt.matshow(M.transpose());

    # plt.colorbar()
    # plt.axis('off')
    # exec("plt.savefig('C:/Users/Ahuch/Documents/GitHub/OEIS/Images/A287864_" + str(n) + ".png')")
    # plt.show()