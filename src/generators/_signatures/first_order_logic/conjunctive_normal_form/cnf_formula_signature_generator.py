from __future__ import annotations

from itertools import chain, product, combinations_with_replacement
from typing import Generator, Dict

from src.ast.first_order_logic import CNFFormula
from src.generators import AstGenerator
from .cnf_clause_signature_generator import CNFClauseSignatureGenerator


class CNFFormulaSignatureGenerator(AstGenerator):
    def __init__(self, clause_gens: Dict[CNFClauseSignatureGenerator, int]):
        """
        :param clause_gens: Dict[clause gen:amount of clauses]
        """
        self.clause_gens = clause_gens

    def generate(self) -> Generator[CNFFormula, None, None]:
        clause_candidates = []
        for clause_gen, n_clause in self.clause_gens.items():
            clause_candidates.append(combinations_with_replacement(clause_gen.generate(), n_clause))
        for clause in product(*clause_candidates):
            yield CNFFormula(items=list(chain(*clause)))
