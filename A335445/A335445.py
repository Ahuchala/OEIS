# Code written by Andy Huchala
# Computes a(n) for OEIS A335445 
# Maximum number of rooks within an n X n chessboard
# where each rook has a path to an edge of the board

# this won't work until I can find a way to avoid cycles in the y_i_j :/

# Requires installing Gurobi

# Select board size 

n = 5

from gurobipy import *
import math
m = Model("ip")


# initialize all variables of form x_i_j
# nonzero values means a rook at (i,j)
for i in range(n):
    for j in range(n):
        exec("x_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j) + "\")")

# initialize all variables of form y_i_j
# nonzero value means there's a rookless path from (i,j) to an edge
for i in range(n):
    for j in range(n):
        exec("y_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"y_" + str(i) + "_" + str(j) + "\")")


# initialize all variables of form z_i_j
# nonzero value means there's a rookless path to (i,j) from an edge, but (i,j) possibly contains a rook
for i in range(n):
    for j in range(n):
        exec("y_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"y_" + str(i) + "_" + str(j) + "\")")
         

# Set objective: maximize sum of x_i_j's

obj = LinExpr(0)
for i in range(n):
    for j in range(n):
            exec("obj.addTerms(1,x_" + str(i) + "_" + str(j) +")")
m.setObjective(obj, GRB.MAXIMIZE)


# if you have a rook then no path can go through you

for i in range(n):
    for j in range(n):
        # y_i_j + x_i_j <= 1
        s = LinExpr(0)
        exec("s.addTerms(1,x_" + str(i) + "_" + str(j) +")")
        exec("s.addTerms(1,y_" + str(i) + "_" + str(j) +")")
        exec("m.addLConstr(s <= 1)")


# rookless edges have a clear path
for i in range(n):
    for j in range(n):
        if i == 0 or j == 0 or i == n-1 or j == n-1:
            exec("model.addGenConstrIndicator(y_" + str(i) + "_" + str(j) + ",False," + "y_" + str(i) + "_" + str(j) + "== 1)") 

# you have a clear path if have access to a rookless edge
for i in range(n):
    for j in range(n):
        if not (i == 0 or j == 0 or i == n-1 or j == n-1):
            # there must be a clear path to a tile with a path out
            # iterate through all tiles that could be threatened

# |       |       |  i,y  |       |
# |_______|_______|_______|_______|
# |       |       |  i,b  |       |
# |       |       |       |       |
# |_______|_______|_______|_______|
# |       |       |       |       |
# |  x,j  |       |  a,j  |  i,j  |
# |_______|_______|_______|_______|

            for x in range(n):
                if x != i:
                    # check if there's a clear path between x and i

                    # example assuming x < a
                    # if sum_{x,i}x_{a,j} == 0:
                    #   y_{i,j} = 1
                    x_sum = LinExpr(0)
                    exec("x_sum.addTerms(1,x_" + str(i) + "_" + str(j) +")")
                    for a in range(min(x,i),max(x,i)):
                        exec("x_sum.addTerms(1,x_" + str(a) + "_" + str(j) +")")
                    # this will be >0 if any of the y_a_j>0 
                    y_sum = LinExpr(0)
                    for a in range(min(x,i),max(x,i)):
                        exec("y_sum.addTerms(1,y_" + str(a) + "_" + str(j) +")")
                    exec("model.addGenConstrIndicator(" + str(x_sum) + ",False," + "y_" + str(i) + "_" + str(j) + ">= " + str(y_sum)+")") 

            for y in range(n):
                if y != j:
                    x_sum = LinExpr(0)
                    exec("x_sum.addTerms(1,x_" + str(i) + "_" + str(j) +")")
                    for b in range(min(j,y),max(j,y)):
                        exec("x_sum.addTerms(1,x_" + str(i) + "_" + str(b) +")")
                    # this will be >0 if any of the y_a_j>0 
                    y_sum = LinExpr(0)
                    for b in range(min(j,y),max(j,y)):
                        exec("y_sum.addTerms(1,y_" + str(i) + "_" + str(b) +")")
                    exec("model.addGenConstrIndicator(" + str(x_sum) + ",False," + "y_" + str(i) + "_" + str(j) + ">= " + str(y_sum)+")") 


# if you have a rook then you must either be an edge or have access to one
for i in range(n):
    for j in range(n):
        if not (i == 0 or j == 0 or i == n-1 or j == n-1):



m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))


print('Obj: %g' % obj.getValue())
