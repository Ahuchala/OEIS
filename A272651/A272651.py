# Code written by Andy Huchala
# Computes a(n) for OEIS A272651
# (The no-3-in-line problem: maximal number of points from 
#  an n X n square grid so that no three lie on a line.)

# Requires installing Gurobi

# Select board size (n>1)
n = 47

import math
from gurobipy import *
m = Model("ip")

# initialize all variables of form x_j_i
for i in range(n):
    for j in range(n):
        exec("x_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j) + "\")")
        

# Set objective: maximize sum of x_i_j's

obj = LinExpr(0)

for i in range(n):
    for j in range(n):
        exec("obj.add(x_" + str(i) + "_" + str(j) +")")

m.setObjective(obj, GRB.MAXIMIZE)


# specify constraints

# all row, column, and diagonal sums must be <= 2

# take all lines of slope y = sx with s = p/q through origin for coprime p,q < n
#    S is the set of points

#    while S nonempty:
#       p = point in S
#       T = all points lying on the line of slope s through p
#       remove T from S
#       if |T| > 2, enforce:
#           sum T <= 2

# Now repeat for negative slopes
# Also include slope 1/0 to represent vertical line

pts = set()
for p in range(n):
    for q in range(n):
        pts.add(tuple([p,q]))

for (p,q) in pts:
    # s = p/q
    if math.gcd(p,q) == 1: # since gcd(0,0) = 0
        S = pts.copy()
        while len(S) > 0:
            P_x, P_y = S.pop()
            # see what points lie on y-P_y = s(x-P_x)
            T = [(i,j) for (i,j) in S if q*(j-P_y) == p*(i-P_x)]
            for pt in T:
                S.remove(pt)
            if len(T)>1:
                l = LinExpr(0)
                for (i,j) in T:
                    exec("l.add(x_" + str(i) + "_" + str(j) +")")
                exec("l.add(x_" + str(P_x) + "_" + str(P_y) +")")
                m.addLConstr(l<=2)

        p *= -1
        S = pts.copy()
        while len(S) > 0:
            P_x, P_y = S.pop()
            # see what points lie on y-P_y = s(x-P_x)
            T = [(i,j) for (i,j) in S if q*(j-P_y) == p*(i-P_x)]
            for pt in T:
                S.remove(pt)
            if len(T)>1:
                l = LinExpr(0)
                for (i,j) in T:
                    exec("l.add(x_" + str(i) + "_" + str(j) +")")
                exec("l.add(x_" + str(P_x) + "_" + str(P_y) +")")
                m.addLConstr(l<=2)


m.optimize()

# for v in m.getVars(): 
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())

# uncomment this to plot


# import numpy as np
# import matplotlib.pyplot as plt

# plt.rcParams["figure.figsize"] = (10,10)

# M = np.zeros((n,n))

# nonzero_vars = [a for a in m.getVars() if a.x > 0]
# for a in nonzero_vars:
#     foo,i,j = str(a).split("_")
#     i = int(i)
#     j = int(j.split(" ")[0])
#     M[i][j] = 1
# # for j in range(n):
# #     for i in range(j,2*n-j-1):
# #         if m.getVar("x_" + str(i) + "_" + str(j)).x > 0:
# #             print(i,j)
# #         else:
# #             print(m.getVarByName("x_" + str(i) + "_" + str(j)))
# #         M[i][j] = int(0.1+m.getVarByName("x_" + str(i) + "_" + str(j)).x)+1


# plt.matshow(M.transpose());

# # plt.colorbar()
# plt.axis('off')
# plt.show()