from __future__ import annotations

from itertools import combinations
from typing import Iterable, Generator

from src.ast.first_order_logic import CNFClause


class CNFClauseGenerator:
    def __init__(self, clause_lengths: Iterable[int], literal_gen: LiteralGenerator):
        self.clause_lengths = set(clause_lengths)
        self.literal_gen = literal_gen

    def generate(self) -> Generator[CNFClause, None, None]:
        for clause_len in self.clause_lengths:
            for n_args in combinations(self.literal_gen.generate(), clause_len):
                yield CNFClause(items=n_args)
