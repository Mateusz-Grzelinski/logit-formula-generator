from __future__ import annotations

from itertools import combinations

from src.ast.first_order_logic import *


class CNFFormulaGenerator:
    def __init__(self, clause_gen: CNFClauseGenerator):
        self.clause_gen = clause_gen

    def generate(self, number_of_clauses: int):
        # this problem can be solved using Branch and cut - integer linear programming
        # x1*cnf_length1 + x2*cnf_length2 + ... = number_of_literals
        for clause in combinations(self.clause_gen.generate(), number_of_clauses):
            yield CNFFormula(items=clause)
