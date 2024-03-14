# Code written by Andy Huchala
# Computes a(n) for OEIS A279404 
# (the minimum queens required to occupy xor
#  threaten all tiles on a toroidal n x n chessboard)

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
        for k in range(n):
            if k != j:
                s += "x_" + str(k) + "_" + str(i) + ","
            if k != i:
                s += "x_" + str(j) + "_" + str(k) + ","
            if k != j or (i-j+k)%n != i: 
                s += "x_" + str(k) + "_" + str((i-j+k)%n) + ","
            if k != j or (2*i-(i-j+k))%n != i:
                s += "x_" + str(k) + "_" + str((2*i-(i-j+k))%n) + ","

        s = s[:-1]

        exec(s+ "]), \"" + "y_" + str(j) + "_" + str(i) + "\")")
for j in range(n):
    for i in range(n):
        exec("m.addConstr(x_" + str(j) + "_" + str(i) + "+ y_" + str(j) + "_" + str(i) +" ==1)")

m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())