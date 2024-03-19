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


r = -1
# r is some upper bound on path length
if n < 10:
    r = [-1,0, 0, 2, 5, 10, 17, 24, 35, 47][n]

# or bound by 1 (??) plus best known results from https://www.mayhematics.com/t/2n.htm
else:
    r = 5+[-1,0, 0, 2, 5, 10, 17, 24, 35, 47,61,76,94,106,135,183,211,238,268,302,337,374,414,455,499,542,588,638,689,743,789,772]
if (n >= 10):
    print("Warning: answer may not be optimal, just improves on known bounds")

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
        print(i,j)
        
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
# for i in range(n):
#     for j in range(n):
#         print(i,j)
#         var_ij = []
#         for a in range(-2,3):
#             for b in range(-2,3):
#                 if (abs(a) == 2 and abs(b) ==1) or (abs(a) == 1 and abs(b) == 2):
#                     if 0 <= i-a < n and 0 <= j-b < n:
#                         var_ij.append((i-a,j-b))


# |       | c,d   |       |       |
# |_______|_______|_______|_______|
# |       |       |       |       |
# | a,b   |       |       |  e,f  |
# |_______|_______|_______|_______|
# |       |       |       |       |
# |       |       |  i,j  |       |
# |_______|_______|_______|_______|


        for (a,b) in var_ij:

            # run through all lines between points in range(min(a,i)-2,max(a,i)+3) 
            #                                         range(min(b,j)-2,max(b,j)+3) 
            # see if their intersection is in the interval [min(a,i),max(a,i)]
            #                                              [min(b,j),max(b,j)]
            
            for c in range(max(min(a,i)-2,0),min(max(a,i)+3,n)):
                for d in range(max(min(b,j)-2,0),min(max(b,j)+3,n)):
                    if (c,d) != (a,b) and (c,d) != (i,j):
                        for e in range(max(min(a,i)-2,0),min(max(a,i)+3,n)):
                            for f in range(max(min(b,j)-2,0),min(max(b,j)+3,n)):
                                if ((e,f) != (a,b) and (e,f) != (i,j)) and (e,f) != (c,d):
                                    if abs(c-e) + abs(d-f) == 3:
                                        if (b*c - a*d - b*e + a*f + d*i - f*i - c*j + e*j) != 0:


                                            # line between  (a,b) <-> (i,j)
                                            # y = x(b-j)/(a-i) + (aj-bi)/(a-i)

                                            # line between  (c,d) <-> (e,f)
                                            # y = x(d-f)/(c-e) + (cf-de)/(c-e)

                                            # intersect at 
                                            # x = (-a d e + a c f + b c i - b e i + d e i - c f i - a c j + a e j)/(b c - a d - b e + a f + d i - f i - c j + e j)
                                            # y = (-b d e + b c f + b d i - b f i - a d j + d e j + a f j - c f j)/(b c - a d - b e + a f + d i - f i - c j + e j)
                                            x0 = (-a*d*e + a*c*f + b*c*i - b*e*i + d*e*i - c*f*i - a*c*j + a*e*j)/(b*c - a*d - b*e + a*f + d*i - f*i - c*j + e*j)
                                            y0 = (-b*d*e + b*c*f + b*d*i - b*f*i - a*d*j + d*e*j + a*f*j - c*f*j)/(b*c - a*d - b*e + a*f + d*i - f*i - c*j + e*j)

                                            if min(a,i) <= x0 <= max(a,i) and min(b,j) <= y0 <= max(b,j):
                                                if min(c,e) <= x0 <= max(c,e) and min(d,f) <= y0 <= max(d,f):
                                                # must exclude simultaneous pairs (a,b),(i,j),(c,d),(e,f)
                                                    for k in range(1,r):
                                                        for l in range(1,r):
                                                            s   = "x_" + str(i) + "_" + str(j) + "_" + str(k) + "+"
                                                            s  += "x_" + str(a) + "_" + str(b) + "_" + str(k-1) + "+"
                                                            s  += "x_" + str(c) + "_" + str(d) + "_" + str(l) + "+"
                                                            s  += "x_" + str(e) + "_" + str(f) + "_" + str(l-1)
                                                            exec("m.addLConstr(" + s + "<= 3)")
                                                            s   = "x_" + str(i) + "_" + str(j) + "_" + str(k-1) + "+"
                                                            s  += "x_" + str(a) + "_" + str(b) + "_" + str(k) + "+"
                                                            s  += "x_" + str(c) + "_" + str(d) + "_" + str(l) + "+"
                                                            s  += "x_" + str(e) + "_" + str(f) + "_" + str(l-1)
                                                            exec("m.addLConstr(" + s + "<= 3)")
                                                            s   = "x_" + str(i) + "_" + str(j) + "_" + str(k) + "+"
                                                            s  += "x_" + str(a) + "_" + str(b) + "_" + str(k-1) + "+"
                                                            s  += "x_" + str(c) + "_" + str(d) + "_" + str(l-1) + "+"
                                                            s  += "x_" + str(e) + "_" + str(f) + "_" + str(l)
                                                            exec("m.addLConstr(" + s + "<= 3)")
                                                            s   = "x_" + str(i) + "_" + str(j) + "_" + str(k-1) + "+"
                                                            s  += "x_" + str(a) + "_" + str(b) + "_" + str(k) + "+"
                                                            s  += "x_" + str(c) + "_" + str(d) + "_" + str(l-1) + "+"
                                                            s  += "x_" + str(e) + "_" + str(f) + "_" + str(l)
                                                            exec("m.addLConstr(" + s + "<= 3)")


m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))

print('Obj: %g' % obj.getValue())