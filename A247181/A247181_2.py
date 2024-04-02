# makes b-file

# Code written by Andy Huchala
# Computes a(n) for OEIS A247181 
# ( Total domination number of the n-hypercube graph.)

# ((equivalently, the size of minimal binary covering code of length n-1 and covering radius 1.))
# Requires installing Gurobi


from gurobipy import *
import math
ls = [0]
for _ in range(15):
    ls.append(0)
# Select board width (n>1)
from gurobipy import *
import math
m = Model("ip")

for n in range(1,16):


        
    # make a set of nodes
    vars_i = []


    # initialize all variables of form x_i
    for i in range(2**n):
        
        exec("x_" + str(i) + " = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"x_" + str(i) +"\")")
        # exec("y_" + str(i) + "_" + str(j)+" = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=\"y_" + str(i) + "_" + str(j) + "\")")


                
    # Set objective: minimize sum of x_i_j's


    t = ""

    for i in range(2**n):
        t += "+x_" + str(i)
    t = t[1:]
            
    exec("obj = " + t)
    m.setObjective(obj, GRB.MINIMIZE)


    # specify constraints
    for i in range(2**n):
        # find all the locations from which (i,j) could be attacked, add each one to the constraint
        # for (i,j): (i,j) must be attacked or occupied
        
        s = "m.addLConstr("
        
        # adjacent nodes differ by a single bit
        dir_list = [int(format((i ^ (1 << k)),'b'),2) for k in range(n+1)]

        # s += "x_" + str(i) + "+"

        for a in dir_list:
            if a < 2**n:
                 s += "x_" + str(a) +"+"
            

        s = s[:-1]

        exec(s+ ">=1)")

        # s = "m.addGenConstrOr("
        # s += "y_" + str(i) + "_" + str(j) + ", ["
        
        # for (a,b) in dir_list:
        #     if (a,b) in vars_ij:
        #          s += "x_" + str(a) + "_" + str(b) + ","
            

        # s = s[:-1]

        # exec(s+ "])")
        # exec("m.addLConstr(x_" + str(i) + "_" + str(j) + "+y_" + str(i) + "_" + str(j) + "<= 1)")


    m.optimize()

    # for v in m.getVars():
    #     print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % obj.getValue())
    ls[n] = int(0.5 + obj.getValue())
    print(n,ls[n])
    print(ls)





