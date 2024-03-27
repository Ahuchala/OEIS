# This version appears slightly slower

# Code written by Andy Huchala
# Computes a(n) for OEIS A003192 
# max length of uncrossed knight's path on an n X n board.

# Requires installing Gurobi

# Select board size (n>3)

n = 5

from gurobipy import *
import math
m = Model("ip")


r = -1
# r is some upper bound on path length
# add one from A003192[n] since I'm secretly using it for vertex count
if n < 10:
    r = 1+[-1,0, 0, 2, 5, 10, 17, 24, 35, 47][n]

# or bound by 1 (??) plus best known results from https://www.mayhematics.com/t/2n.htm
else:
    r = 2+[-1,0, 0, 2, 5, 10, 17, 24, 35, 47,61,76,94,106,135,183,211,238,268,302,337,374,414,455,499,542,588,638,689,743,789,772]
if (n >= 10):
    print("Warning: answer may not be optimal, just improves on known bounds")

# initialize all variables of form x_i_j_k
# nonzero values mean the kth step was at point (i,j)
for i in range(n):
    for j in range(n):
        for k in range(r):
            exec("x_" + str(i) + "_" + str(j)+"_" + str(k)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) + "_" + str(j)+ "_" + str(k) + "\")")
            
            
# Set objective: maximize sum of x_i_j_k's

obj = LinExpr(-1)
for i in range(n):
    for j in range(n):
        for k in range(r):
            exec("obj.addTerms(1,x_" + str(i) + "_" + str(j) + "_" + str(k)+")")
m.setObjective(obj, GRB.MAXIMIZE)


# only allow one occupied tile per step

for k in range(r):
    s = LinExpr(0)
    for i in range(n):
        for j in range(n):
            exec("s.addTerms(1,x_" + str(i) + "_" + str(j) + "_" + str(k) +")")

    exec("m.addLConstr(s<= 1)")

# only occupy each tile once
for i in range(n):
    for j in range(n):
        s = LinExpr(0)
        for k in range(r):
            exec("s.addTerms(1,x_" + str(i) + "_" + str(j) + "_" + str(k) + ")")
        exec("m.addLConstr(s<= 1)")


# find all the locations from which (i,j) could be attacked, add each one to the constraint
for i in range(n):
    for j in range(n):
        print(i,j)
        
        var_ij = []
        for (a,b) in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
            if 0 <= i-a and i-a < n and 0 <= j-b  and j-b < n:
        # # for a in range(-2,3): 
        # #     for b in range(-2,3):
        #         if abs(a) + abs(b) == 3 and 0 <= i-a < n and 0 <= j-b < n:
                var_ij.append((i-a,j-b))
        for k in range(1,r):
            s = LinExpr(0)
            for (a,b) in var_ij:
                exec("s.addTerms(1,x_" + str(a) + "_" + str(b)+ "_" + str(k-1) +")")
            exec("m.addLConstr(" + "x_" + str(i) + "_" + str(j)+ "_" + str(k) + "<= s)")


# enforce non crossing

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
            #          and same for (c,d), (e,f)

            # can always assume a < i
            # if a < i:
            min_ai = a; max_ai = i; # min_ai = min(a,i); max_ai = max(a,i)
            min_bj = min(b,j); max_bj = max(b,j)
            max_min_ai_minus_2 = max(min_ai-2,0)
            min_max_ai_plus_3 = min(max_ai+3,n)
            max_min_bj_minus_2 = max(min_bj-2,0)
            min_max_bj_plus_3 = min(max_bj+3,n)
            for c in range(max_min_ai_minus_2,min_max_ai_plus_3):
                for d in range(max_min_bj_minus_2,min_max_bj_plus_3):
                    # must exclude simultaneous pairs (a,b),(i,j),(c,d),(e,f)
                    # if (c,d) != (a,b) and (c,d) != (i,j):
                    if (c != a or d != b) and (c != i or d != j):
                        # can always assume c < e
                        max_c_plus_one = max(c+1,max_min_ai_minus_2)
                        for e in range(max_c_plus_one,min_max_ai_plus_3):
                            
                            min_ce = c; max_ce = e
                            # min(c,e) max(c,e)
                            
                            for f in range(max_min_bj_minus_2,min_max_bj_plus_3):
                                if (e != a or f != b) and (e != i or f != j):
                                # if ((e,f) != (a,b) and (e,f) != (i,j)):# and (e,f) != (c,d):
                                    if (c-e)**2 + (d-f)**2 == 5:
                                        if (b*c - a*d - b*e + a*f + d*i - f*i - c*j + e*j) != 0: # if lines not parallel


    # line between    (a,b) <-> (i,j)           y = x(b-j)/(a-i) + (aj-bi)/(a-i)
    # line between    (c,d) <-> (e,f)           y = x(d-f)/(c-e) + (cf-de)/(c-e)

                                            # intersect at 
                                            x0 = (-a*d*e + a*c*f + b*c*i - b*e*i + d*e*i - c*f*i - a*c*j + a*e*j)/(b*c - a*d - b*e + a*f + d*i - f*i - c*j + e*j)
                                            y0 = (-b*d*e + b*c*f + b*d*i - b*f*i - a*d*j + d*e*j + a*f*j - c*f*j)/(b*c - a*d - b*e + a*f + d*i - f*i - c*j + e*j)


                                            if min_ai < x0 and x0 < max_ai and min_bj < y0 and y0 < max_bj:
                                            # if min_ai <= x0 <= max_ai and min(b,j) <= y0 <= max(b,j):
                                                min_df = min(d,f); max_df = max(d,f)
                                                if min_ce < x0 and x0 < max_ce and min_df < y0 and y0 < max_df:
                                                    for k in range(1,r): #can assume k > l
                                                        for l in range(1,k):
                                                            # if k != l:
                                                            exec("s = LinExpr( x_" + str(i) + "_" + str(j) + "_" + str(k)+")")
                                                            exec("s.addTerms(1,x_" + str(a) + "_" + str(b) + "_" + str(k-1) + ")")
                                                            exec("s.addTerms(1,x_" + str(c) + "_" + str(d) + "_" + str(l) + ")")
                                                            exec("s.addTerms(1,x_" + str(e) + "_" + str(f) + "_" + str(l-1) + ")")
                                                            m.addLConstr(s <= 3)
                                                            exec("s = LinExpr( x_" + str(i) + "_" + str(j) + "_" + str(k-1)+")")
                                                            exec("s.addTerms(1,x_" + str(a) + "_" + str(b) + "_" + str(k) + ")")
                                                            exec("s.addTerms(1,x_" + str(c) + "_" + str(d) + "_" + str(l) + ")")
                                                            exec("s.addTerms(1,x_" + str(e) + "_" + str(f) + "_" + str(l-1) + ")")
                                                            m.addLConstr(s <= 3)
                                                            exec("s = LinExpr( x_" + str(i) + "_" + str(j) + "_" + str(k)+")")
                                                            exec("s.addTerms(1,x_" + str(a) + "_" + str(b) + "_" + str(k-1) + ")")
                                                            exec("s.addTerms(1,x_" + str(c) + "_" + str(d) + "_" + str(l-1) + ")")
                                                            exec("s.addTerms(1,x_" + str(e) + "_" + str(f) + "_" + str(l) + ")")
                                                            m.addLConstr(s <= 3)
                                                            exec("s = LinExpr( x_" + str(i) + "_" + str(j) + "_" + str(k-1)+")")
                                                            exec("s.addTerms(1,x_" + str(a) + "_" + str(b) + "_" + str(k) + ")")
                                                            exec("s.addTerms(1,x_" + str(c) + "_" + str(d) + "_" + str(l-1) + ")")
                                                            exec("s.addTerms(1,x_" + str(e) + "_" + str(f) + "_" + str(l) + ")")
                                                            m.addLConstr(s <= 3)


m.optimize()

# for v in m.getVars():
#     print('%s %g' % (v.varName, v.x))


print('Obj: %g' % obj.getValue())
if obj.getValue() == r-1 and n > 9:
    print("Warning: answer may not be optimal, just improves on known bounds")


# uncomment this to plot
# ijk_list = []
# printstr = ""
# for i in range(n):
#     for j in range(n):
#         for k in range(r):
#             v = m.getVarByName("x_" + str(i) + "_" + str(j) + "_" + str(k))
#             if int(v.x+0.4) > 0:
# #                 x,i,j,k = str(v).split("_")

# #                 k = int(k.split(" (")[0])
# #                 i = int(i)
# #                 j = int(j)
#                 ijk_list.append((i,j,k))
# #         printstr += str(int(v.x))
# import numpy as np
# import matplotlib.pyplot as plt

# plt.rcParams["figure.figsize"] = (10,10)


# xy_ls = sorted(ijk_list,key = lambda blah : blah[2])

# # plt.colorbar()
# plt.axis('off')

# for i in range(len(xy_ls)-1):
#     plt.plot([xy_ls[i][0],xy_ls[i+1][0]],[xy_ls[i][1],xy_ls[i+1][1]])

# for _ in range(n):
#     for __ in range(n):
#         plt.plot(_,__,'bo')