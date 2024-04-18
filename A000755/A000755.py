# Code written by Andy Huchala
# Computes a(n) for OEIS A000755
# ( No-3-in-line problem on n X n grid:
#   total number of ways of placing 2n 
#   points on n X n grid so no 3 are in a line. 
#   No symmetries are taken into account.

# Requires installing cplex

# Select board size (n>1)
n = 7

MAX_VALUE = 4000000 # upper bound on a(n)
PRINT_SOLUTION = True # whether or not to print the objective and an example solution

from docplex.mp.model import Model
import cplex

print("Computing A103315(n) for n =", str(n))

# this function ripped from https://stackoverflow.com/questions/60759169/how-to-increase-number-of-cplex-solutions
def generate_soln_pool(mdl):      
    cpx = mdl.get_cplex()
    cpx.parameters.mip.pool.intensity.set(4)
    cpx.parameters.mip.pool.absgap.set(0.1)
    cpx.parameters.mip.pool.relgap.set(0.1)
    cpx.parameters.mip.limits.populate.set(MAX_VALUE)

    try:
        cpx.populate_solution_pool()
    except CplexSolverError:
        print("Exception raised during populate")
        return []
    numsol = cpx.solution.pool.get_num()
    return(numsol)

    # this will return the actual values
    # nb_vars = mdl.number_of_variables
    # sol_pool = []
    # for i in range(numsol):

    #     x_i = cpx.solution.pool.get_values(i)
    #     assert len(x_i) == nb_vars
    #     sol = mdl.new_solution()
    #     for k in range(nb_vars):
    #         vk = mdl.get_var_by_index(k)
    #         sol.add_var_value(vk, x_i[k])
    #     sol_pool.append(sol)
    # return sol_pool


im = Model(name='ip_3_no_in_line')

for j in range(n):
    for i in range(n):
        exec("x_" + str(j) + "_" + str(i) + " = im.integer_var(0, 1,name=  \"" + "x_" + str(j) + "_" + str(i) + "\")")


s = "x_0_0"
for j in range(n):
    for i in range(n):
        if i + j != 0:
            s += "+ x_"+ str(j) + "_" + str(i)
exec("im.maximize(" + s + ")")

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
            if len(T)>2:
                l = ""
                for (i,j) in T:
                    l += "+x_" + str(i) + "_" + str(j)
                l += "+x_" + str(P_x) + "_" + str(P_y)
                l = l[1:]
                exec("im.add_constraint)" + l + "<=2)")

        p *= -1
        S = pts.copy()
        while len(S) > 0:
            P_x, P_y = S.pop()
            # see what points lie on y-P_y = s(x-P_x)
            T = [(i,j) for (i,j) in S if q*(j-P_y) == p*(i-P_x)]
            for pt in T:
                S.remove(pt)
            if len(T)>2:
                l = ""
                for (i,j) in T:
                    l += "+x_" + str(i) + "_" + str(j)
                l += "+x_" + str(P_x) + "_" + str(P_y)
                l = l[1:]
                exec("im.add_constraint)" + l + "<=2)")

im.solve()
if PRINT_SOLUTION:
    im.print_solution()

print(generate_soln_pool(im))