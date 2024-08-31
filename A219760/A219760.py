# Code written by Andy Huchala
# based on Rob Pratt's suggested IP

# Computes a(n) for OEIS A219760
# (Martin Gardner's minimal no-3-in-a-line problem.
    
# a(n) is the minimal number of counters that can 
# be placed on an n X n chessboard, no three in a line,     
# such that adding one more counter on any vacant square 
# will produce three in a line.

# Requires installing Gurobi

# Select board size (n>1)
n = 34

import math
from gurobipy import *
m = Model("ip")

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

# we'll keep track of the k = 0..len(SQUARES)-1 lines by what points
# they contain
SQUARES = []

# For each point, keep track of which lines go through it
LINES = [[[ ] for _ in range(n)] for _ in range(n)]


for (p,q) in [(1,0),(0,1),(1,1),(1,-1)]:
    # s = p/q
    if math.gcd(p,q) == 1: # since gcd(0,0) = 0
        S = pts.copy()
        while len(S) > 0:
            P_x, P_y = S.pop()
            # see what points lie on y-P_y = s(x-P_x)
            T = [(i,j) for (i,j) in S if q*(j-P_y) == p*(i-P_x)]
            for pt in T:
                S.remove(pt)
            T += [(P_x,P_y)]
            if len(T)>2:

                k = len(SQUARES)
                for (i,j) in T:
                    LINES[i][j] = LINES[i][j] + [k]
                SQUARES.append(T)

# x[i,j] = 1 if a queen appears in square (i,j), 0 otherwise
for i in range(n):
    for j in range(n):
        exec("x_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j) + "\")")
        
# y[k] = 1 if line k contains exactly two queens, 0 otherwise
for k in range(len(SQUARES)):
    exec("y_" + str(k) +" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"y_" + str(k) + "\")")

# Set objective: maximize sum of x_i_j's
obj = LinExpr(0)

for i in range(n):
    for j in range(n):
        exec("obj.add(x_" + str(i) + "_" + str(j) +")")

m.setObjective(obj, GRB.MINIMIZE)
# print(LINES)
# print(SQUARES)

for k in range(len(SQUARES)):
    l = LinExpr(0)
    for (i,j) in SQUARES[k]:
        exec("l.add(x_" + str(i) + "_" + str(j) + ")" )
    exec("m.addLConstr(2 * y_" + str(k) + "<= l)")
    exec("m.addLConstr(l <= 1 + y_" + str(k)+")" )

for i in range(n):
    for j in range(n):
        l = LinExpr(0)
        for k in LINES[i][j]:
            exec("l.add(y_" + str(k) +")")
        exec("m.addLConstr(x_" + str(i) + "_" + str(j) + "+ l>=1)")



m.optimize()

for v in m.getVars(): 
    print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())
