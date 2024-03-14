# Code written by Andy Huchala
# Computes a(n) for OEIS A342576 
# (the minimum knights required to occupy xor
#  threaten all tiles on an n x n chessboard)

# Requires installing Gurobi

# Select board size (n>1)
n = 8

from gurobipy import *
m = Model("ip")

# initialize all variables of form x_j_i
for i in range(n):
    for j in range(n):
        # x_i_j denotes a queen at (i,j)
        exec("x_" + str(j) + "_" + str(i)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(j) + "_" + str(i) + "\")")
        # y_i_j denotes (i,j) being threatened by another queen
        exec("y_" + str(j) + "_" + str(i)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"y_" + str(j) + "_" + str(i) + "\")")
        

# Set objective: minimize sum of x_i_j's

# one = m.addVar(lb=1,ub=1,vtype=GRB.BINARY,name="one")

t = "x_0_0"

for j in range(n):
    for i in range(n):
        if i + j != 0:
            t += "+x_" + str(j) + "_" + str(i)
        
exec("obj = " + t)
m.setObjective(obj, GRB.MINIMIZE)


# specify constraints
for j in range(n):
    for i in range(n):
        # find all the locations from which (i,j) could be attacked, add each one to the constraint
        # for (i,j): (i,j) must be attacked xor occupied
        
        s = "m.addConstr("
        s += "y_" + str(j) + "_" + str(i) + "== or_(["
        if (i-2 >= 0):
            if (j-1 >= 0):
                s += "x_" + str(j-1) + "_" + str(i-2) + ","
            if (j+1 < n):
                s += "x_" + str(j+1) + "_" + str(i-2) + ","
        if (i-1 >= 0):
            if (j-2 >= 0):
                s += "x_" + str(j-2) + "_" + str(i-1) + ","
            if (j+2 < n):
                s += "x_" + str(j+2) + "_" + str(i-1) + ","
        if (i+2 < n):
            if (j-1 >= 0):
                s += "x_" + str(j-1) + "_" + str(i+2) + ","
            if (j+1 < n):
                s += "x_" + str(j+1) + "_" + str(i+2) + ","
        if (i+1 < n):
            if (j-2 >= 0):
                s += "x_" + str(j-2) + "_" + str(i+1) + ","
            if (j+2 < n):
                s += "x_" + str(j+2) + "_" + str(i+1) + ","

        s = s[:-1]

        exec(s+ "]), \"" + "c_" + str(j) + "_" + str(i) + "\")")
for j in range(n):
    for i in range(n):
        exec("m.addConstr(x_" + str(j) + "_" + str(i) + "+ y_" + str(j) + "_" + str(i) +" ==1)")

m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())