# Code written by Andy Huchala
# Computes a(n) for OEIS A002564
# (the number of ways to arrange a minimal number
#  of queens which threaten all tiles on an n x n chessboard)

# Requires installing cplex

# Select board size (n>1)
n = 4

MAX_VALUE = 4000000 # upper bound on a(n)
PRINT_SOLUTION = True # whether or not to print the objective and an example solution

from docplex.mp.model import Model
import cplex

print("Computing A002564(n) for n =", str(n))

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


im = Model(name='ip_number_queens')

for j in range(n):
    for i in range(n):
        exec("x_" + str(j) + "_" + str(i) + " = im.integer_var(name=  \"" + "x_" + str(j) + "_" + str(i) + "\")")


s = "x_0_0"
for j in range(n):
    for i in range(n):
        if i + j != 0:
            s += "+ x_"+ str(j) + "_" + str(i)
exec("im.minimize(" + s + ")")

for j in range(n):
    for i in range(n):
        exec("im.add_constraint(x_" + str(j) + "_" + str(i) + " <= 1)")
        exec("im.add_constraint(x_" + str(j) + "_" + str(i) + " >= 0)")


        s = "im.add_constraint("
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
        exec(s+ ">=1)")

im.solve()
if PRINT_SOLUTION:
    im.print_solution()

print(generate_soln_pool(im))