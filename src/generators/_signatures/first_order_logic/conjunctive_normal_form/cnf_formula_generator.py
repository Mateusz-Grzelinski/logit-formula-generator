from __future__ import annotations

from typing import Dict

from src.ast.first_order_logic import CNFFormula
from src.generators import AstGenerator
from .cnf_clause_generator import CNFClauseGenerator


class CNFFormulaGenerator(AstGenerator):
    def __init__(self, clause_gens: Dict[CNFClauseGenerator, int]):
        """
        :param clause_gens: Dict[clause gen:amount of clauses]
        """
        self.clause_gens = clause_gens

    def generate(self) -> CNFFormula:
        f = CNFFormula(items=[])
        for clause_gen, n_clause in self.clause_gens.items():
            f.extend(clause_gen.generate() for i in range(n_clause))
        return f
