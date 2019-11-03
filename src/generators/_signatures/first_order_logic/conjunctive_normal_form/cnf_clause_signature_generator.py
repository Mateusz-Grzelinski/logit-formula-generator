from __future__ import annotations

from itertools import combinations_with_replacement
from random import randint
from typing import Iterable, Generator

from src.ast.first_order_logic import CNFClause
from src.generators import AstGenerator


class CNFClauseSignatureGenerator(AstGenerator):
    def __init__(self, clause_lengths: Iterable[int], literal_gen: LiteralGenerator):
        self.allowed_clause_lengths = set(clause_lengths)
        self.allowed_clause_lengths.discard(0)
        self.literal_gen = literal_gen

    def generate(self) -> Generator[CNFClause, None, None]:
        def clause_with_defined_length(length: int) -> Generator[CNFClause, None, None]:
            for n_args in combinations_with_replacement(self.literal_gen.generate(), length):
                yield CNFClause(items=n_args)

        generators = []
        for clause_len in self.allowed_clause_lengths:
            generators.append(clause_with_defined_length(clause_len))

        while generators:
            index = randint(0, len(generators) - 1)
            try:
                yield next(generators[index])
            except StopIteration:
                del generators[index]
