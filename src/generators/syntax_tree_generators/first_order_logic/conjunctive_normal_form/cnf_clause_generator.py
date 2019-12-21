from __future__ import annotations

import random
from typing import Iterable

from src.ast.first_order_logic import CNFClause
from src.generators import AstGenerator


class CNFClauseGenerator(AstGenerator):
    def __init__(self, clause_lengths: Iterable[int], literal_gen: LiteralSignatureGenerator):
        self.allowed_clause_lengths = list(set(clause_lengths))
        assert 0 not in self.allowed_clause_lengths
        self.literal_gen = literal_gen

    def generate(self) -> CNFClause:
        length = random.choice(self.allowed_clause_lengths)
        c = CNFClause(items=[])
        for i in range(length):
            c.append(self.literal_gen.generate())
        return c
