from __future__ import annotations

from itertools import chain
from typing import Generator, Dict

from src.ast.first_order_logic import CNFFormula
from src.generators import AstGenerator
from src.generators.utils import lazy_product, lazy_combinations_with_replacement, ensure_unique_id
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
            clause_candidates.append(lazy_combinations_with_replacement(clause_gen.generate(), n_clause))
        for clauses in lazy_product(*clause_candidates):
            flatten = list(chain.from_iterable(clauses))
            yield CNFFormula(items=ensure_unique_id(flatten))
