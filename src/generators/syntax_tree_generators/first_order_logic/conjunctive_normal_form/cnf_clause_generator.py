from __future__ import annotations

import random
from typing import Iterable

from src.generators import SyntaxTreeGenerator
from src.syntax_tree.first_order_logic import CNFClause


class CNFClauseGenerator(SyntaxTreeGenerator):
    def __init__(self, clause_lengths: Iterable[int], atom_gen: AtomGenerator):
        self.allowed_clause_lengths = list(set(clause_lengths))
        assert 0 not in self.allowed_clause_lengths
        self.atom_gen = atom_gen

    def generate(self) -> CNFClause:
        length = random.choice(self.allowed_clause_lengths)
        c = CNFClause(children=[])
        for i in range(length):
            c.append(self.atom_gen.generate())
        return c
