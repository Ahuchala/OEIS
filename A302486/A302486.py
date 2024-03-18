# Code written by Andy Huchala
# Computes a(n) for OEIS A302486 
# total domination number of the n-triangular grid graph

# Requires installing Gurobi

# Select board size (n>1)

# currently this computes a(n-1)
n = 10

from gurobipy import *
import math
m = Model("ip")


# example with n = 4
#  __
# /  \__
# \__/j \___
# /-i\__/i+j\__
# \__/0 \___/  \
# /  \__/i  \__/
# \__/-j\___/
# /  \__/
# \__/

#  __
# /  \__
# \__/01\__
# /-i\__/11\__
# \__/00\__/21\
# /  \__/10\__/
# \__/-j\__/
# /  \__/
# \__/

        
# make a set of admissible (i,j) pairs
# it turns out gurobi doesn't like negative numbers in string so we're adding n to everything
vars_ij = []


# initialize all variables of form x_j_i
for i in range(-n,n+1):
    for j in range(-n,n+1):
        if i - j <= (n+1) //3 and j <= n //3 and i >= -((n-1)//3):
            exec("x_" + str(i+n) + "_" + str(j+n)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(j+n) + "_" + str(i+n) + "\")")
            vars_ij.append((i,j))

# beats me why this fails
# @assert(len(vars_ij)==(n*(n+1))//2)
print(len(vars_ij),(n*(n+1))//2)
            
# Set objective: minimize sum of x_i_j's


t = ""

for (i,j) in vars_ij:
    t += "+x_" + str(i+n) + "_" + str(j+n)
t = t[1:]
        
exec("obj = " + t)
m.setObjective(obj, GRB.MINIMIZE)


# specify constraints
for (i,j) in vars_ij:
    # find all the locations from which (i,j) could be attacked, add each one to the constraint
    # for (i,j): (i,j) must be attacked or occupied
    
    s = "m.addLConstr("
    # s += "x_" + str(i+n) + "_" + str(j+n) + "+"
    
#     all the directions a piece can be threatened from
    dir_list = [(i-1,j),(i,j-1),(i+1,j),(i,j+1),(i-1,j-1),(i+1,j+1)]

    
    for (a,b) in dir_list:
        if (a,b) in vars_ij:
             s += "x_" + str(a+n) + "_" + str(b+n) + "+"
        

    s = s[:-1]

    exec(s+ ">=1)")


m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())