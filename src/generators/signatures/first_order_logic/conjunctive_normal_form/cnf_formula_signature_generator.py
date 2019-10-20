from __future__ import annotations

from itertools import combinations, chain, product
from typing import Generator

from src.ast.first_order_logic import CNFFormula
from src.generators.contraint_solver.z3_solver import Z3ConstraintSolver
from src.generators.range import Range
from .cnf_clause_signature_generator import CNFClauseSignatureGenerator


class CNFFormulaSignatureGenerator:
    def __init__(self, clause_gen: CNFClauseSignatureGenerator):
        self.clause_gen = clause_gen

    def generate(self, number_of_clauses: Range, number_of_literals: Range) -> Generator:
        solver = Z3ConstraintSolver(allowed_clause_lengths=self.clause_gen.allowed_clause_lengths,
                                    number_of_clauses=number_of_clauses,
                                    number_of_literals=number_of_literals)
        # todo randomize solutions?
        for solution in solver.solve():
            clause_candidates = {}
            for clause_len, n_clause in solution.items():
                clause_candidates[clause_len] = combinations(self.clause_gen.generate(clause_len), n_clause)
            for clause in product(*clause_candidates.values()):
                skip_solution = yield CNFFormula(items=list(chain(*clause)))
                if skip_solution:
                    break
