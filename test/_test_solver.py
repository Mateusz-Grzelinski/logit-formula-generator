import logging
import time
from pprint import pprint

from src.generators import IntegerRange
from src.generators._contraint_solver.z3_solver import Z3ConstraintSolver


class TestZ3ConstraintSolver:
    def test_solutions(self):
        # not really a test
        solver = Z3ConstraintSolver(
            clause_lengths=[1, 2, ],
            number_of_clauses=IntegerRange(min=10, max=20),
            number_of_literals=IntegerRange(min=10, max=40)
        )
        solutions = list(solver.solve_in_random_order())
        print()
        pprint(solutions)

    def test_big_example(self):
        # todo: takes hours to complete, but is should yield solutions incrementally
        solver = Z3ConstraintSolver(
            clause_lengths=[1, 12, 100],
            # number_of_clauses=IntegerRange.from_relative(number=100, min_delta=50),
            # number_of_literals=IntegerRange.from_relative(number=5000, min_delta=100)
            number_of_clauses=IntegerRange(min=30, max=100),
            number_of_literals=IntegerRange(min=100, max=3000)
        )
        # note pytest will block printing to stdout
        print()
        start = time.time()
        for sol in solver.solve():
            print(sol)
            logging.info(sol)
        else:
            print('None found')
        print(f'It took {time.time() - start} to compute')
