# Code written by Andy Huchala
# Computes a(n) for OEIS A002564
# (the number of ways to arrange a minimal number
#  of queens which threaten all tiles on an n x n chessboard)

# Requires installing Gurobi

# Select board size (n>1)
n = 12


num_runs = 100 #upper bound on a[n]

A075458 = [-1, 1, 1, 1, 2, 3, 3, 4, 5, 5, 5, 5, 6, 7, 8, 9, 9, 9, 9, 10, 11, 11, 12, 12, 13, 13]
import math
from gurobipy import *

solutions = []
for run in range(num_runs):
    

    m = Model("ip")

    # initialize all variables of form x_j_i
    for i in range(n):
        for j in range(n):
            exec("x_" + str(j) + "_" + str(i)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(j) + "_" + str(i) + "\")")

    for i in range(num_runs):
        exec("y_" + str(i) + " = m.addVar(lb=0,ub=1,vtype=GRB.BINARY, name=\"y_" + str(i) + "\")")

    # Set objective: minimize sum of x_i_j's

    t = "x_0_0"

    for j in range(n):
        for i in range(n):
            if i + j != 0:
                t += "+x_" + str(j) + "_" + str(i)

    exec("obj = " + t)
    m.setObjective(obj, GRB.MINIMIZE)

    exec("m.addLConstr( " + str(t) + " == " + str(A075458[n]) + ")")

    for sol in solutions:
        t = sol[0]
        for _ in range(len(sol)):
            t += " , " + str(sol[_])

        exec("m.addGenConstrAnd(y_" + str(i) + ",[" + str(t) + "])")
        exec("m.addLConstr(y_" + str(i) + "==0)")

    # specify constraints
    for j in range(n):
        for i in range(n):
            # find all the locations from which (i,j) could be attacked, add each one to the constraint
            # for (i,j): (i,j) must be attacked or occupied

            s = "m.addLConstr("
            s += "x_" + str(j) + "_" + str(i) + "+"
            for k in range(n):
                if k != j:
                    s += "x_" + str(k) + "_" + str(i) + "+"
                if k != i:
                    s += "x_" + str(j) + "_" + str(k) + "+"
                if i-j+k>=0 and i-j+k<n:
                    if k != j or (i-j+k) != i: 
                        s += "x_" + str(k) + "_" + str(i-j+k) + "+"
                if 2*i-(i-j+k)>=0 and 2*i-(i-j+k)<n:
                    if k != j or 2*i-(i-j+k) != i:
                        s += "x_" + str(k) + "_" + str(2*i-(i-j+k)) + "+"

            s = s[:-1]

            exec(s+ ">=1, \"" + "c_" + str(j) + "_" + str(i) + "\")")

    m.optimize()

    # for v in m.getVars():
    #     print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % obj.getValue())
    #     solutions.append(['or_([%s<= %g,%s>= %g]' % (v.varName, v.x) for v in m.getVars()])
    new_sol = ['%s %g' % (v.varName, v.x) for v in m.getVars()]
    nonzero_var = []
    for var in new_sol:
        a,b = var.split(' ')
        if int(b) != 0:
            nonzero_var.append(a)
    solutions.append(nonzero_var)
    