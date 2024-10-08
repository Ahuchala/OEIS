# makes b-file

# Code written by Andy Huchala
# Computes a(n) for OEIS A251532 
# ( Independence number of the n-triangular 
#   honeycomb obtuse knight graph)

# Requires installing Gurobi


import sys
sys.setrecursionlimit(5000)

ls = [0]
ls += [1, 3, 6, 7, 7, 9, 15, 18, 21, 21, 27, 31, 36, 42, 42, 47, 54, 62, 70, 70, 77, 85, 95, 105, 109, 117, 126, 136, 147, 155, 166, 176, 187, 199, 210, 222, 235, 247, 260, 274, 287, 301, 316, 330, 345, 361, 376, 392, 409, 425, 442, 460, 477, 495, 514, 532, 551, 571, 590, 610, 631, 651, 672, 694, 715, 737, 760, 782, 805, 829, 852, 876, 901, 925, 950, 976, 1001, 1027, 1054, 1080, 1107, 1135, 1162, 1190, 1219, 1247, 1276, 1306, 1335, 1365, 1396, 1426, 1457, 1489, 1520, 1552, 1585, 1617, 1650, 1684, 1717, 1751, 1786, 1820, 1855, 1891, 1926, 1962, 1999, 2035, 2072, 2110, 2147, 2185, 2224, 2262, 2301, 2341, 2380, 2420, 2461, 2501, 2542, 2584, 2625, 2667, 2710, 2752, 2795, 2839, 2882, 2926, 2971, 3015, 3060, 3106, 3151, 3197, 3244, 3290, 3337, 3385, 3432, 3480, 3529, 3577, 3626, 3676, 3725, 3775, 3826, 3876, 3927, 3979, 4030, 4082, 4135, 4187, 4240, 4294, 4347, 4401, 4456, 4510, 4565, 4621, 4676, 4732, 4789, 4845, 4902, 4960, 5017, 5075, 5134, 5192, 5251, 5311, 5370, 5430, 5491, 5551, 5612, 5674, 5735, 5797, 5860, 5922, 5985, 6049, 6112, 6176, 6241, 6305, 6370, 6436, 6501, 6567, 6634, 6700, 6767, 6835, 6902, 6970, 7039, 7107, 7176, 7246, 7315, 7385, 7456, 7526, 7597, 7669, 7740, 7812, 7885, 7957, 8030, 8104, 8177, 8251, 8326, 8400, 8475, 8551, 8626, 8702, 8779, 8855, 8932, 9010, 9087, 9165, 9244, 9322, 9401, 9481, 9560, 9640, 9721, 9801, 9882, 9964, 10045, 10127, 10210, 10292, 10375, 10459, 10542, 10626, 10710, 10795, 10880, 10966, 11051, 11137, 11224, 11310, 11397, 11485, 11572, 11660, 11748, 11837, 11926, 12016, 12105, 12195, 12285, 12376, 12467, 12559, 12650, 12742]
for _ in range(300):
    ls.append(0)
# Select board width (n>1)
from gurobipy import *
import math
m = Model("ip")

for n in range(len(ls)-300,len(ls)):



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



    #            __
    #         __/  \__  
    #      __/**\__/**\__  
    #   __/**\__/  \__/**\__
    #  /  \__/  \__/  \__/  \
    #  \__/  \__/  \__/02\__/  
    #  /**\__/  \__/01\__/12\
    #  \__/  \__/00\__/11\__/  
    #  /**\__/  \__/10\__/21\
    #  \__/  \__/  \__/  \__/  
    #  /  \__/  \__/  \__/  \
    #  \__/**\__/  \__/**\__/
    #     \__/**\__/**\__/
    #        \__/  \__/
    #           \__/



    # make a set of admissible (i,j) pairs
    vars_ij = []


    # initialize all variables of form x_j_i
    for i in range(n):
        for j in range(n-i):
            exec("x_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j) + "\")")
            exec("y_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"y_" + str(i) + "_" + str(j) + "\")")

            vars_ij.append((i,j))

    # beats me why this fails
    # @assert(len(vars_ij)==(n*(n+1))//2)
#     print(len(vars_ij),(n*(n+1))//2)

    # Set objective: minimize sum of x_i_j's


    
    t = LinExpr(0)

    for (i,j) in vars_ij:
        exec("t.add(x_" + str(i) + "_" + str(j) + ")")
    # t = t[1:]

    obj = t

    m.setObjective(obj, GRB.MAXIMIZE)



    # specify constraints
    for (i,j) in vars_ij:
        # find all the locations from which (i,j) could be attacked, add each one to the constraint
        # for (i,j): (i,j) must be attacked or occupied

        s = "m.addGenConstrOr("
        s += "y_" + str(i) + "_" + str(j) + ", ["

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
                 s += "x_" + str(a) + "_" + str(b) + ","


        s = s[:-1]

        exec(s+ "])")
        exec("m.addLConstr(x_" + str(i) + "_" + str(j) + "+y_" + str(i) + "_" + str(j) + "<= 1)")


    m.optimize()

    # for v in m.getVars():
    #     print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % obj.getValue())
    ls[n] = int(0.5 + obj.getValue())
    print(n,ls[n])
    print(ls)