# Code written by Andy Huchala
# Computes a(n) for OEIS A087329 
# independence number for KT_4 knight
# on hexagonal board

# Requires installing Gurobi

# Select board size (n>3)

n = 8

from gurobipy import *
import math
m = Model("ip")

# KT_4 knight hexagon graph has adjacencies as below
#            __
#         __/  \__  
#      __/**\__/**\__  
#   __/**\__/  \__/**\__
#  /  \__/**\__/**\__/  \
#  \__/  \__/  \__/  \__/  
#  /**\__/  \__/  \__/**\
#  \__/**\__/00\__/**\__/  
#  /**\__/  \__/  \__/**\
#  \__/  \__/  \__/  \__/  
#  /  \__/**\__/**\__/  \
#  \__/**\__/  \__/**\__/
#     \__/**\__/**\__/
#        \__/  \__/
#           \__/
#         
# x_ij indxed like below for n = 4
#        __
#     __/  \__
#  __/  \__/02\
# /  \__/01\__/
# \__/00\__/11\
# /  \__/10\__/
# \__/  \__/20\
#    \__/  \__/
#       \__/     

        
# make a set of admissible (i,j) pairs
# it turns out gurobi doesn't like negative numbers in string so we're adding n to everything
vars_ij = []


# initialize all variables of form x_j_i
for i in range(int((-n+1)/2),int((n+2)/2)):
    for j in range(int((-n+1)/2),int((n+2)/2)):
        if i + j <= (n) //2 and -i - j < (n+1) //2:
            exec("x_" + str(i+n) + "_" + str(j+n)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i+n) + "_" + str(j+n) + "\")")
            exec("y_" + str(i+n) + "_" + str(j+n)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i+n) + "_" + str(j+n) + "\")")
            
            vars_ij.append((i,j))


# print(len(vars_ij),math.ceil(n**2 * 3/4))
            
# Set objective: minimize sum of x_i_j's


t = ""

for (i,j) in vars_ij:
    t += "+x_" + str(i+n) + "_" + str(j+n)
t = t[1:]
        
exec("obj = " + t)
m.setObjective(obj, GRB.MAXIMIZE)


# specify constraints
for (i,j) in vars_ij:
    # find all the locations from which (i,j) could be attacked, add each one to the constraint
    # for (i,j): (i,j) must be attacked or occupied
    
    s = "m.addGenConstrOr("
    s += "y_" + str(i+n) + "_" + str(j+n) + ",["
    
#     all the directions a piece can be threatened from
    dir_list = [(i+1,j+1),(i+2,j+1),(i+1,j+2),
                (i-1,j+2),(i-1,j+3),(i-2,j+3),
                (i-2,j+1),(i-3,j+1),(i-3,j+2),
                
                (i-1,j-1),(i-2,j-1),(i-1,j-2),
                (i+1,j-2),(i+1,j-3),(i+2,j-3),
                (i+2,j-1),(i+3,j-1),(i+3,j-2),
               ]

    
    for (a,b) in dir_list:
        if (a,b) in vars_ij:
             s += "x_" + str(a+n) + "_" + str(b+n) + ","
        

    s = s[:-1]

    exec(s+ "])")
    exec("m.addLConstr(" + "x_" + str(i+n) + "_" + str(j+n) + "+ y_" + str(i+n) + "_" + str(j+n) + "<=1)")


m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())