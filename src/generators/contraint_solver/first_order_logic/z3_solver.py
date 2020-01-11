# https://stackoverflow.com/questions/46840912/how-to-solve-a-system-of-linear-equations-over-the-nonnegative-integers
import math
from typing import Iterable, Dict

import z3

from src.generators.contraint_solver.first_order_logic.cnf_constraint_solver import CNFConstraintSolver
from src.generators.utils._range import IntegerRange


class Z3CNFConstraintSolver(CNFConstraintSolver):
    def __init__(self, clause_lengths: Iterable[int], number_of_clauses: IntegerRange,
                 number_of_literals: IntegerRange):
        super().__init__(list(clause_lengths), number_of_clauses, number_of_literals)

    def solve(self) -> Iterable[Dict[int, int]]:
        A = self.literal_coefficients
        n = len(A)
        X = [z3.Int('x%d' % i) for i in range(n)]
        s = z3.Solver()

        # solutions must be positive
        s.add(z3.And([X[i] >= 0 for i in range(n)]))

        # clauses must be in range
        # s.add(z3.Sum([A.clauses_coeff[j] * X[j] for j in range(n)]) == int(self.number_of_clauses.average))
        if self.number_of_clauses.max != math.inf:
            s.add(z3.Sum(X) <= self.number_of_clauses.max)
        if self.number_of_clauses.min != -math.inf:
            s.add(z3.Sum(X) >= self.number_of_clauses.min)

        # literals must be in range
        # s.add(z3.Sum([A.literal_coeff[j] * X[j] for j in range(n)]) == int(self.number_of_literals.average))
        if self.number_of_literals.max != math.inf:
            s.add(z3.Sum([A[j] * X[j] for j in range(n)]) <= self.number_of_literals.max)
        if self.number_of_literals.min != -math.inf:
            s.add(z3.Sum([A[j] * X[j] for j in range(n)]) >= self.number_of_literals.min)

        # print(f'{s.model()=}')
        while s.check() == z3.sat:
            solution = [s.model().evaluate(X[i]) for i in range(n)]
            yield {clause_len: s.as_long() for clause_len, s in zip(self.literal_coefficients, solution) if
                   s.as_long() != 0}
            forbid = z3.Or([X[i] != solution[i] for i in range(n)])
            s.add(forbid)


if __name__ == '__main__':
    z3solver = Z3CNFConstraintSolver(clause_lengths=[1, 2, 3], number_of_clauses=IntegerRange(min=5, max=10),
                                     number_of_literals=IntegerRange(min=7, max=20))
    for solution in z3solver.solve_in_random_order():
        print(f'{solution}')
