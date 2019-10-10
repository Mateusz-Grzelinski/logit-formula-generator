# https://stackoverflow.com/questions/46840912/how-to-solve-a-system-of-linear-equations-over-the-nonnegative-integers

from z3 import *

A = [[2, 2, 5], [1, 1, 1]]
b = [1000, 500]
n = len(A[0])  # number of variables
m = len(b)  # number of constraints

X = [Int('x%d' % i) for i in range(n)]
s = Solver()
s.add(And([X[i] >= 0 for i in range(n)]))
for i in range(m):
    s.add(Sum([A[i][j] * X[j] for j in range(n)]) == b[i])

while s.check() == sat:
    print(s.model())
    sol = [s.model().evaluate(X[i]) for i in range(n)]
    forbid = Or([X[i] != sol[i] for i in range(n)])
    s.add(forbid)
