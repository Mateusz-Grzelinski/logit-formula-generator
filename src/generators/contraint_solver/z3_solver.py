# https://stackoverflow.com/questions/46840912/how-to-solve-a-system-of-linear-equations-over-the-nonnegative-integers
from typing import List, Iterable, Dict

import z3

from src.generators.contraint_solver.constraint_solver import ConstraintSolver
from src.generators.range import Range


class Z3ConstraintSolver(ConstraintSolver):

    def __init__(self, allowed_clause_lengths: List, number_of_clauses: Range, number_of_literals: Range):
        super().__init__(list(allowed_clause_lengths), number_of_clauses, number_of_literals)

    def solve(self) -> Iterable[Dict[int, int]]:
        A = self.coefficients
        n = len(A)  # number of variables

        X = [z3.Int('x%d' % i) for i in range(n)]

        s = z3.Solver()
        # solutions must be positive
        s.add(z3.And([X[i] >= 0 for i in range(n)]))

        # clauses must be in range
        # s.add(z3.Sum([A.clauses_coeff[j] * X[j] for j in range(n)]) == int(self.number_of_clauses.average))
        s.add(z3.Sum([A.clauses_coeff[j] * X[j] for j in range(n)]) <= self.number_of_clauses.max)
        s.add(z3.Sum([A.clauses_coeff[j] * X[j] for j in range(n)]) >= self.number_of_clauses.min)

        # literals must be in range
        # s.add(z3.Sum([A.literal_coeff[j] * X[j] for j in range(n)]) == int(self.number_of_literals.average))
        s.add(z3.Sum([A.literal_coeff[j] * X[j] for j in range(n)]) <= self.number_of_literals.max)
        s.add(z3.Sum([A.literal_coeff[j] * X[j] for j in range(n)]) >= self.number_of_literals.min)

        # print(f'{s.model()=}')
        while s.check() == z3.sat:
            solution = [s.model().evaluate(X[i]) for i in range(n)]
            forbid = z3.Or([X[i] != solution[i].as_long() for i in range(n)])
            s.add(forbid)
            yield {clause_len: s.as_long() for clause_len, s in zip(self.coefficients.literal_coeff, solution) if
                   s.as_long() != 0}


if __name__ == '__main__':
    z3solver = Z3ConstraintSolver(allowed_clause_lengths=[1, 2, 3], number_of_clauses=Range(min=5, max=10),
                                  number_of_literals=Range(min=7, max=20))
    for solution in z3solver.solve():
        print(f'{solution=}')
