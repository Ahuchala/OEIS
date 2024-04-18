# Code for tuning the gurobi model


# Code written by Andy Huchala
# Computes a(n) for OEIS A006075
# (the minimum knights required to cover (threaten or occupy) all tiles
#    on an n x n chessboard)

# Select board size
n = 15

# This implementation uses the MIP solver Gurobi
from gurobipy import *
m = Model("ip")

# initialize all variables of form x_j_i
for i in range(n):
    for j in range(n):
        exec("x_" + str(j) + "_" + str(i)+" = m.addVar(lb=0,ub=1,vtype=GRB.BINARY, name=\"x_" + str(j) + "_" + str(i) + "\")")

# Set objective: minimize sum of x_i_j's

t = "x_0_0"

for j in range(n):
    for i in range(n):
        if i + j != 0:
            t += "+x_" + str(j) + "_" + str(i)
        
exec("obj = " + t)
m.setObjective(obj, GRB.MINIMIZE)


# specify constraints
for i in range(n):
    for j in range(n):
        var_ij = []
        for a in range(-2,3):
            for b in range(-2,3):
                if abs(a) + abs(b) == 3 and 0 <= i-a < n and 0 <= j-b < n:
                    var_ij.append((i-a,j-b))
        s = ""
        for (a,b) in var_ij:
            s += "x_" + str(a) + "_" + str(b) + "+"
        s = s[:-1]
        exec("m.addLConstr(" + "x_" + str(i) + "_" + str(j) + "+" + str(s) + ">=1)")



m.optimize()

# for v in m.getVars():
    # print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())
# m.optimize()
m.setParam("TuneCriterion", 0)
m.setParam("TuneTimeLimit", 1000)
m.tune()
