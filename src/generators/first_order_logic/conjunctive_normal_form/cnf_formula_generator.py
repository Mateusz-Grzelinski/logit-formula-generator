from __future__ import annotations

from src.generators.first_order_logic.conjunctive_normal_form.cnf_clause_generator import CNFClauseGenerator
from src.generators.range import Range


class CNFFormulaGenerator:
    def __init__(self, clause_gen: CNFClauseGenerator):
        self.clause_gen = clause_gen

    def generate(self, number_of_clauses: Range, number_of_literals: Range):
        # this problem can be solved using Branch and cut - integer linear programming
        # x1*cnf_length1 + x2*cnf_length2 + ... in number_of_literals
        # x1 + x2 + ... in number_of_clauses
        # for clause in combinations(self.clause_gen.generate(), number_of_clauses):
        #     yield CNFFormula(items=clause)
        partitions = None

    def solve(self, number_of_clauses: Range, number_of_literals: Range):
        pass
        # start from biggest clause
        # @dataclass(frozen=True)
        # class Properties:
        #     number_of_literals: int

        # clauses: Dict[int, int] = {}
        # for clause_len in sorted(self.clause_gen.clause_lengths, reverse=True):
        #     clauses[clause_len] = 0
        #     if clauses[] * clause_len in number_of_literals:
        #         yield
        # import mip
        # mip.Solver
