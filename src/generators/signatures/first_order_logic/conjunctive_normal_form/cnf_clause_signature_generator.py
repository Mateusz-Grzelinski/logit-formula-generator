from __future__ import annotations

from itertools import combinations
from typing import Iterable, Generator

from src.ast.first_order_logic import CNFClause


class CNFClauseSignatureGenerator:
    def __init__(self, clause_lengths: Iterable[int], literal_gen: LiteralGenerator):
        self.allowed_clause_lengths = set(clause_lengths)
        self.literal_gen = literal_gen

    def generate(self, clause_length: int = None) -> Generator[CNFClause, None, None]:
        if clause_length:
            for n_args in combinations(self.literal_gen.generate(), clause_length):
                yield CNFClause(items=n_args)
        else:
            for clause_len in self.allowed_clause_lengths:
                for n_args in combinations(self.literal_gen.generate(), clause_len):
                    yield CNFClause(items=n_args)
