from __future__ import annotations

from typing import Dict

from src.generators import SyntaxTreeGenerator
from src.syntax_tree.first_order_logic import CNFFOLFormula
from .cnf_clause_generator import CNFClauseGenerator


class CNFFormulaGenerator(SyntaxTreeGenerator):
    def __init__(self, clause_gens: Dict[CNFClauseGenerator, int]):
        """
        :param clause_gens: Dict[clause gen:amount of clauses]
        """
        self.clause_gens = clause_gens

    def generate(self) -> CNFFOLFormula:
        f = CNFFOLFormula(children=[])
        for clause_gen, n_clause in self.clause_gens.items():
            f.extend(clause_gen.generate() for i in range(n_clause))
        return f
