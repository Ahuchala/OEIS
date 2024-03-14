# goal: compute A002564

n = 4

poly_ieqs = []
# add inequalities; [1,3,4,6,7] means 1 + 3x00 + 4x01 + 6x10 + 7x11 >= 0

# bound all variables
for j in range(n):
    for i in range(n):
        l = [0 for _ in range(n**2+1)]
        l[0] = 1
        l[1+j*n + i] = -1
        poly_ieqs.append(l)
        l = [0 for _ in range(n**2+1)]
        l[0] = 0
        l[1+j*n + i] = 1
        poly_ieqs.append(l)

# inequalities for threatened tiles
for j in range(n):
    for i in range(n):
        l = [0 for _ in range(n**2+1)]
        l[0] = -1
        for k in range(n):
            if k != j:
                l[1+k*n + i] = 1
            if k != i:
                l[1+j*n + k] = 1
            if i-j+k>=0 and i-j+k<n:
                if k != j or (i-j+k) != i: 
                    l[1+k*n + i-j+k] = 1
            if 2*i-(i-j+k)>=0 and 2*i-(i-j+k)<n:
                if k != j or 2*i-(i-j+k) != i:
                    l[1+k*n + 2*i-(i-j+k)] = 1
        poly_ieqs.append(l)


        
# equality for sum, based on A075458
A075458 = [-1, 1, 1, 1, 2, 3, 3, 4, 5, 5, 5, 5, 6, 7, 8, 9, 9, 9, 9, 10, 11, 11, 12, 12, 13, 13]
l = [1 for _ in range(n**2+1)]
l[0] = -A075458[n]
poly_ieqs.append(l)
l = [-_ for _ in l]
poly_ieqs.append(l)

# then run these commands in polymake
print("$p = new Polytope(INEQUALITIES=>" + str(poly_ieqs) + ");")
print("print $p->LATTICE_POINTS;")