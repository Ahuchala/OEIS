# Code written by Andy Huchala
# Computes a(n) for OEIS A264041 

# a(n) is the maximum number of diagonals that can be placed in 
# an n X n grid made up of 1 X 1 unit squares when diagonals are 
# placed in the unit squares in such a way that no two diagonals 
# may cross or intersect at an endpoint.

# Requires installing Gurobi


n = 4

from gurobipy import *
import math
m = Model("ip")

# a(n) is the size of a maximum independent set in a graph with vertices 
# (x,y,z), x=1..n, y=1..n, z=1..2, with edges joining (x,y,z) to (x,y,3-z), 
# (x+1,y,3-z), and (x,y+1,3-z), (x,y,1) to (x+1,y-1,1) and (x,y,2) to (x+1,y+1,2).
#                  - Robert Israel, Nov 01 2015

        


# initialize all variables of form x_i_j_k
for i in range(n):
    for j in range(n):
        for k in range(2):
            exec(f"x_{i}_{j}_{k} = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = \"x_{i}_{j}_{k}\")")

            
# Set objective: maximize sum of x_i_j_k's



obj = LinExpr(0)
for i in range(n):
    for j in range(n):
        for k in range(2):
            exec(f"obj.add(x_{i}_{j}_{k})")


m.setObjective(obj, GRB.MAXIMIZE)


# specify constraints

# edges joining (x,y,z) to (x,y,3-z), 
# (x+1,y,3-z), and (x,y+1,3-z),
 # (x,y,1) to (x+1,y-1,1) 
 # and (x,y,2) to (x+1,y+1,2).


for i in range(n):
    for j in range(n):

        constraint = LinExpr(0)
        exec(f"constraint.add(x_{i}_{j}_{0})")
        exec(f"constraint.add(x_{i}_{j}_{1})")
        exec(f"m.addLConstr(constraint <= 1)")

        for k in range(2):
            if i < n-1:
                constraint = LinExpr(0)
                exec(f"constraint.add(x_{i}_{j}_{k})")
                exec(f"constraint.add(x_{i+1}_{j}_{1-k})")
                exec(f"m.addLConstr(constraint <= 1)")

            if j < n-1:
                constraint = LinExpr(0)
                exec(f"constraint.add(x_{i}_{j}_{k})")
                exec(f"constraint.add(x_{i}_{j+1}_{1-k})")
                exec(f"m.addLConstr(constraint <= 1)")

        if i < n-1 and j > 0:
            constraint = LinExpr(0)
            exec(f"constraint.add(x_{i}_{j}_{0})")
            exec(f"constraint.add(x_{i+1}_{j-1}_{0})")
            exec(f"m.addLConstr(constraint <= 1)")

        if i < n-1 and j < n-1:
            constraint = LinExpr(0)
            exec(f"constraint.add(x_{i}_{j}_{1})")
            exec(f"constraint.add(x_{i+1}_{j+1}_{1})")
            exec(f"m.addLConstr(constraint <= 1)")

m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())

