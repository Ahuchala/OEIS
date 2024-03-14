# Code written by Andy Huchala
# Computes a(n) for OEIS A308632 
# (the largest aggressor given
#  maximal peaceable armies of queens)

# Requires installing Gurobi

# Select board size (n>1)
n = 8


A250000 = [-1, 0, 0, 1, 2, 4, 5, 7, 9, 12, 14, 17, 21, 24, 28, 32]
import math
from gurobipy import *
m = Model("ip")

# white queens x, black queens y
# initialize all variables of form x_j_i, y_j_i
# lowercase means occupied, uppercase means threatened
for i in range(n):
    for j in range(n):
        exec("x_" + str(j) + "_" + str(i)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(j) + "_" + str(i) + "\")")
        exec("y_" + str(j) + "_" + str(i)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"y_" + str(j) + "_" + str(i) + "\")")
        exec("X_" + str(j) + "_" + str(i)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"X_" + str(j) + "_" + str(i) + "\")")
        exec("Y_" + str(j) + "_" + str(i)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"Y_" + str(j) + "_" + str(i) + "\")")
        

# Set objective: minimize sum of x_i_j's

t = "x_0_0"

for j in range(n):
    for i in range(n):
        if i + j != 0:
            t += "+x_" + str(j) + "_" + str(i)
        
exec("obj = " + t)
m.setObjective(obj, GRB.MAXIMIZE)


# specify constraints

# may have more white queens than black; black fixed by A250000
t = "y_0_0"
for j in range(n):
    for i in range(n):
        if i + j != 0:
            t += "+y_" + str(j) + "_" + str(i)
exec("m.addLConstr(" + t + "== " + str(A250000[n]) + ")")

for j in range(n):
    for i in range(n):
        # find all the locations from which (i,j) could be attacked, add each one to the constraint
        # for (i,j): (i,j) must may be attacked by one color or occupied by the other
        
        s = "m.addConstr("
        s += " X_" + str(j) + "_" + str(i) + "==or_([x_" + str(j) + "_" + str(i) + ","
        for k in range(n):
            if k != j:
                s += "x_" + str(k) + "_" + str(i) + ","
            if k != i:
                s += "x_" + str(j) + "_" + str(k) + ","
            if i-j+k>=0 and i-j+k<n:
                if k != j or (i-j+k) != i: 
                    s += "x_" + str(k) + "_" + str(i-j+k) + ","
            if 2*i-(i-j+k)>=0 and 2*i-(i-j+k)<n:
                if k != j or 2*i-(i-j+k) != i:
                    s += "x_" + str(k) + "_" + str(2*i-(i-j+k)) + ","

        s = s[:-1]
        exec(s+ "])" + ", \"" + "c_" + str(j) + "_" + str(i) + "\")")
        exec("m.addLConstr(X_" + str(j) + "_" + str(i) + " + y_" + str(j) + "_" + str(i) + "<= 1)")


for j in range(n):
    for i in range(n):
        # find all the locations from which (i,j) could be attacked, add each one to the constraint
        # for (i,j): (i,j) must may be attacked by one color or occupied by the other
        
        s = "m.addConstr("
        s += " Y_" + str(j) + "_" + str(i) + "==or_([y_" + str(j) + "_" + str(i) + ","
        for k in range(n):
            if k != j:
                s += "y_" + str(k) + "_" + str(i) + ","
            if k != i:
                s += "y_" + str(j) + "_" + str(k) + ","
            if i-j+k>=0 and i-j+k<n:
                if k != j or (i-j+k) != i: 
                    s += "y_" + str(k) + "_" + str(i-j+k) + ","
            if 2*i-(i-j+k)>=0 and 2*i-(i-j+k)<n:
                if k != j or 2*i-(i-j+k) != i:
                    s += "y_" + str(k) + "_" + str(2*i-(i-j+k)) + ","

        s = s[:-1]
        exec(s+ "])" + ", \"" + "c_" + str(j) + "_" + str(i) + "\")")
        exec("m.addLConstr(Y_" + str(j) + "_" + str(i) + " + x_" + str(j) + "_" + str(i) + "<= 1)")


m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())