from mip.model import *

m = Model()
rhs = 10
coefficients = [2, 2, 5]
n = len(coefficients)

x = [m.add_var(var_type=INTEGER) for i in range(n)]

m.objective = xsum(coefficients[i] * x[i] for i in range(n)) == 10
# m += xsum(coefficients[i] * x[i] for i in range(n))
m += xsum(x) == 5

# to force new solution:
m += x[0] <= 4

# m += 2 >= sum(x)  # total number of clauses (min)
m.optimize()
# print(m.status)
for v in m.vars:
    print('{} : {}'.format(v.name, v.x))
