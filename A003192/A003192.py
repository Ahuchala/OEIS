# Code written by Andy Huchala
# Computes a(n) for OEIS A003192 
# max length of uncrossed knight's path on an n X n board.

# Requires installing Gurobi

# Select board size (n>3)

n = 5

from gurobipy import *
import math
m = Model("ip")


        
# make a set of admissible (i,j) pairs
# it turns out gurobi doesn't like negative numbers in string so we're adding n to everything
vars_ij = []

r = 15
# r is some upper bound on path length


# initialize all variables of form x_i_j_k
# nonzero values mean the kth step was at point (i,j)
for i in range(n):
    for j in range(n):
        for k in range(r):
            exec("x_" + str(i) + "_" + str(j)+"_" + str(k)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j)+ "_" + str(k) + "\")")
            
            
# Set objective: maximize sum of x_i_j_k's


t = ""

for i in range(n):
    for j in range(n):
        for k in range(r):
            t += "+x_" + str(i) + "_" + str(j)+"_" + str(k)
t = t[1:]
        
exec("obj = " + t)
m.setObjective(obj, GRB.MAXIMIZE)


# only allow one occupied tile per step
for k in range(r):
    s = ""
    for i in range(n):
        for j in range(n):
            s += "x_" + str(i) + "_" + str(j) + "_" + str(k) + "+"

    s = s[:-1]
    exec("m.addLConstr(" + str(s) + "<= 1)")

# only occupy each tile once

for i in range(n):
    for j in range(n):
        s = ""
        for k in range(r):
            s += "x_" + str(i) + "_" + str(j) + "_" + str(k) + "+"
        s = s[:-1]
        exec("m.addLConstr(" + str(s) + "<= 1)")




# find all the locations from which (i,j) could be attacked, add each one to the constraint
for i in range(n):
    for j in range(n):
        var_ij = []
        for a in range(-2,3):
            for b in range(-2,3):
                if abs(a) + abs(b) == 3 and 0 <= i-a < n and 0 <= j-b < n:
                    var_ij.append((i-a,j-b))
        for k in range(1,r):
            s = ""
            for (a,b) in var_ij:
                s += "x_" + str(a) + "_" + str(b)+ "_" + str(k-1) + "+"
            s = s[:-1]
            exec("m.addLConstr(" + "x_" + str(i) + "_" + str(j)+ "_" + str(k) + "<=" + str(s) + ")")


# enforce non crossing
# for each edge between x_k and x_{k+1}, there are 8 intersecting edges to rule out


# for each point, add noncrossing constraints
for i in range(n):
    for j in range(n):
        var_ij = []
        for a in range(-2,3):
            for b in range(-2,3):
                if abs(a) + abs(b) == 3 and 0 <= i-a < n and 0 <= j-b < n:
                    var_ij.append((i-a,j-b))

        for (a,b) in var_ij:
            intersect_loci = []
            for x in range(i-1,i+2):
                for y in range(j-1,j+2):
                    if abs(i-x)**2 + abs(j-y)**2+abs(a-x)**2+ abs(b-y)**2 == 3:
                        intersect_loci.append((x,y))
                        # this should contain exactly 2 points by the end
            
            assert len(intersect_loci)==2

            # decide (x1,y1) is the one adjacent to (i-a,j-b)
            #        (x2,y2) is the one adjacent to (i,j)
            x1,y1 = intersect_loci[0]
            x2,y2 = intersect_loci[1]

            if not (x1 == a or y1 == b):
                x1,y1 = intersect_loci[1]
                x2,y2 = intersect_loci[0]

            assert(x1 == a or y1 == b)

# |  O    |       |  O    |       |
# |_______|_______|_______|_______|
# |       |       |       |       |
# | a,b   | x1,y1 |       |   O   |
# |_______|_______|_______|_______|
# |       |       |       |       |
# |       | x2,y2 |  i,j  |       |
# |_______|_______|_______|_______|

            for k in range(1,r):

                s  = "x_" + str(i) + "_" + str(j) + "_" + str(k) + "+"
                s += "x_" + str(a) + "_" + str(b) + "_" + str(k-1) + "+"
                # edges are undirected
                s += "x_" + str(i) + "_" + str(j) + "_" + str(k-1) + "+"
                s += "x_" + str(a) + "_" + str(b) + "_" + str(k) + "+"
    #           (x2,y2) <--> (2*x1-i,2*y1-j) edge must be removed
    #           (x2,y2) <--> (2*x1-a,y1-j) edge must be removed
    #           (x2,y2) <--> (2*x1-a,y1-j) edge must be removed
                for (X1,Y1) in [(a,2*y1-y2), (i,2*y1-y2),(2*i-x2,b)]:
                    if 0 <= X1 < n and 0 <= Y1 < n:
                        for l in range(1,r):
                            t  = "x_" + str(X1) + "_" + str(Y1) + "_" + str(l) + "+"
                            t += "x_" + str(x2) + "_" + str(y2) + "_" + str(l-1) + "+"
                            t += "x_" + str(X1) + "_" + str(Y1) + "_" + str(l-1) + "+"
                            t += "x_" + str(x2) + "_" + str(y2) + "_" + str(l)
                            exec("m.addLConstr(" + s + t + "<= 3)")


# |       |       |       |       |       |
# |_______|_______|_______|_______|_______|
# |       |       |       |       |       |
# |       | a,b   | x1,y1 |       |       |
# |_______|_______|_______|_______|_______|
# |       |       |       |       |       |
# |   O   |       | x2,y2 |  i,j  |       |
# |_______|_______|_______|_______|_______|
# |       |       |       |       |       |
# |       |  O    |       |  O    |       |
# |_______|_______|_______|_______|_______|

            for k in range(1,r):

                s  = "x_" + str(i) + "_" + str(j) + "_" + str(k) + "+"
                s += "x_" + str(a) + "_" + str(b) + "_" + str(k-1) + "+"
                # edges are undirected
                s += "x_" + str(i) + "_" + str(j) + "_" + str(k-1) + "+"
                s += "x_" + str(a) + "_" + str(b) + "_" + str(k) + "+"
    #           (x2,y2) <--> (2*x1-i,2*y1-j) edge must be removed
    #           (x2,y2) <--> (2*x1-a,y1-j) edge must be removed
    #           (x2,y2) <--> (2*x1-a,y1-j) edge must be removed
                for (X1,Y1) in [(a,2*y2-y1), (i,2*y2-y1),(2*a-x1,j)]:
                    if 0 <= X1 < n and 0 <= Y1 < n:
                        for l in range(1,r):
                            t  = "x_" + str(X1) + "_" + str(Y1) + "_" + str(l) + "+"
                            t += "x_" + str(x1) + "_" + str(y1) + "_" + str(l-1) + "+"
                            t += "x_" + str(X1) + "_" + str(Y1) + "_" + str(l-1) + "+"
                            t += "x_" + str(x1) + "_" + str(y1) + "_" + str(l)
                            exec("m.addLConstr(" + s + t + "<= 3)")

# |_______|_______|_______|_______|_______|
# |       |       |       |       |       |
# |       |       | u2,v2 |       |       |
# |_______|_______|_______|_______|_______|
# |       |       |       |       |       |
# |       | a,b   | x1,y1 | u4,v4 |       |
# |_______|_______|_______|_______|_______|
# |       |       |       |       |       |
# |       | u1,v1 | x2,y2 |  i,j  |       |
# |_______|_______|_______|_______|_______|
# |       |       |       |       |       |
# |       |       | u3,v3 |       |       |
# |_______|_______|_______|_______|_______|


            for k in range(1,r):
                s  = "x_" + str(i) + "_" + str(j) + "_" + str(k) + "+"
                s += "x_" + str(a) + "_" + str(b) + "_" + str(k-1) + "+"
                # edges are undirected
                s += "x_" + str(i) + "_" + str(j) + "_" + str(k-1) + "+"
                s += "x_" + str(a) + "_" + str(b) + "_" + str(k) + "+"
    #           (u1,v1) <--> (u2,v2) edge must be removed
    #           (u3,v3) <--> (u4,v4) edge must be removed
    #           (u1,v1) <--> (u4,v4) edge must be removed
                for (X1,Y1,X2,Y2) in [(a,j,x1,2*y1-y2), (x2,2*y2-y1,i,b),(a,j,i,b)]:
                    if 0 <= X1 < n and 0 <= Y1 < n and 0 <= X2 < n and 0 <= Y2 < n:
                        for l in range(1,r):
                            t  = "x_" + str(X1) + "_" + str(Y1) + "_" + str(l) + "+"
                            t += "x_" + str(X2) + "_" + str(Y2) + "_" + str(l-1) + "+"
                            t += "x_" + str(X1) + "_" + str(Y1) + "_" + str(l-1) + "+"
                            t += "x_" + str(X2) + "_" + str(Y2) + "_" + str(l)
                            exec("m.addLConstr(" + s + t + "<= 3)")


m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())