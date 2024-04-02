# Code written by Andy Huchala
# Computes a(n) for OEIS A269706
# ( Domination number of the 
#   n x n x n grid graph.)

# Requires installing Gurobi



# Select board size
n = 5

from gurobipy import *
import math
m = Model("ip")


        
# make a set of admissible (i,j,k) tuples (nodes)
vars_ijk = []


# initialize all variables of form x_i_j_k
for i in range(n):
    for j in range(n):
        for k in range(n):
            exec("x_" + str(i) + "_" + str(j)+"_" + str(k)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j)+"_" + str(k) + "\")")
            exec("y_" + str(i) + "_" + str(j)+"_" + str(k)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"y_" + str(i) + "_" + str(j) +"_" + str(k)+ "\")")

            vars_ijk.append((i,j,k))

            
# Set objective: minimize sum of x_i_j's


t = ""

for (i,j,k) in vars_ijk:
    t += "+x_" + str(i) + "_" + str(j)+ "_" + str(k)
t = t[1:]
        
exec("obj = " + t)
m.setObjective(obj, GRB.MINIMIZE)


# specify constraints
for (i,j,k) in vars_ijk:
    # find all the locations from which (i,j) could be attacked, add each one to the constraint
    # for (i,j): (i,j) must be attacked or occupied
    
    s = "m.addLConstr("
    
#   list all adjacencies
    dir_list = [(i-1,j,k), (i+1,j,k),
                (i,j-1,k), (i,j+1,k),
                (i,j,k-1), (i,j,k+1)
               ]

    s += "x_" + str(i) + "_" + str(j) + "_" + str(k) + "+"

    for (a,b,c) in dir_list:
        if (a,b,c) in vars_ijk:
             s += "x_" + str(a) + "_" + str(b) + "_" + str(c) + "+"
        

    s = s[:-1]

    exec(s+ ">=1)")

    # s = "m.addGenConstrOr("
    # s += "y_" + str(i) + "_" + str(j) + "_" + str(k) + ", ["
    
    # for (a,b,c) in dir_list:
    #     if (a,b,c) in vars_ijk:
    #          s += "x_" + str(a) + "_" + str(b) + "_" + str(c) + ","
        

    # s = s[:-1]

    # exec(s+ "])")
    # exec("m.addLConstr(x_" + str(i) + "_" + str(j) + "_" + str(k)+ "+y_" + str(i) + "_" + str(j) + "_" + str(k)+ "<= 1)")


m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())

