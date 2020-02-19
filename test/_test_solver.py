import logging
import time
from pprint import pprint

from logic_formula_generator.generators import IntegerRange
from logic_formula_generator.generators._contraint_solver.first_order_logic.z3_solver import Z3CNFConstraintSolver


class TestZ3ConstraintSolver:
    """These test run too long to run normally"""
    def test_solutions(self):
        # not really a test
        solver = Z3CNFConstraintSolver(
            clause_lengths=[1, 2, ],
            number_of_clauses=IntegerRange(min=10, max=20),
            number_of_literals=IntegerRange(min=10, max=40)
        )
        solutions = list(solver.solve_in_random_order())
        print()
        pprint(solutions)

    def test_big_example(self):
        # todo: takes hours to complete, but is should yield solutions incrementally
        solver = Z3CNFConstraintSolver(
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
