# makes b-file

# Code written by Andy Huchala
# Computes a(n) for OEIS A342374 
# ( Total domination number of n-triangular 
#   honeycomb obtuse knight graph)
# makes b-file

# Requires installing Gurobi

import sys
sys.setrecursionlimit(5000)
# Select board size (n>4)
ls = [0]
ls += [8, 7, 7, 8, 9, 12, 15, 17, 19, 20, 21, 24, 25, 28, 31, 34, 37, 39, 42, 45]
for _ in range(100):
    ls.append(0)
# Select board width (n>1)
from gurobipy import *
import math
m = Model("ip")
for n in range(25,25+100):

    # example with n = 4
    #  __
    # /  \__
    # \__/  \__
    # /  \__/  \__
    # \__/  \__/  \
    # / j\__/  \__/
    # \__/ i\__/
    # / 0\__/
    # \__/

    # example with n = 4
    #  __
    # / 0\__
    # \_3/ 1\__
    # / 0\_2/ 2\__
    # \_2/ 1\_1/ 3\
    # / 0\_1/ 2\_0/
    # \_1/ 1\_0/
    # / 0\_0/
    # \_0/


    # honeycomb obtuse knight graph has adjacencies as below
    #            __
    #         __/  \__  
    #      __/**\__/**\__  
    #   __/**\__/  \__/**\__
    #  /  \__/  \__/  \__/  \
    #  \__/  \__/  \__/  \__/  
    #  /**\__/  \__/  \__/**\
    #  \__/  \__/00\__/  \__/  
    #  /**\__/  \__/  \__/**\
    #  \__/  \__/  \__/  \__/  
    #  /  \__/  \__/  \__/  \
    #  \__/**\__/  \__/**\__/
    #     \__/**\__/**\__/
    #        \__/  \__/
    #           \__/
    #         



    # make a set of admissible (i,j) pairs
    vars_ij = []


    # initialize all variables of form x_j_i
    for i in range(n):
        for j in range(n-i):
            exec("x_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j) + "\")")

            vars_ij.append((i,j))

    assert(len(vars_ij)==(n*(n+1))//2)

    # Set objective: minimize sum of x_i_j's


    t = ""

    for (i,j) in vars_ij:
        t += "+x_" + str(i) + "_" + str(j)
    t = t[1:]

    exec("obj = " + t)
    m.setObjective(obj, GRB.MINIMIZE)


    # specify constraints
    for (i,j) in vars_ij:
        # find all the locations from which (i,j) could be attacked, add each one to the constraint
        # for (i,j): (i,j) must be attacked or occupied

        s = "m.addLConstr("
        # s += "x_" + str(i) + "_" + str(j) + "+"

    #     all the directions a piece can be threatened from
        dir_list = [(i+2,j+1),(i+1,j+2),
                    (i-1,j+3),(i-2,j+3),
                    (i-3,j+1),(i-3,j+2),

                    (i-2,j-1),(i-1,j-2),
                    (i+1,j-3),(i+2,j-3),
                    (i+3,j-1),(i+3,j-2),
                   ]


        for (a,b) in dir_list:
            if (a,b) in vars_ij:
                 s += "x_" + str(a) + "_" + str(b) + "+"


        s = s[:-1]

        exec(s+ ">=1)")


    m.optimize()

    # for v in m.getVars():
    #     print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % obj.getValue())
    ls[n] = int(0.5 + obj.getValue())
    print(n,ls[n])
    print(ls)

