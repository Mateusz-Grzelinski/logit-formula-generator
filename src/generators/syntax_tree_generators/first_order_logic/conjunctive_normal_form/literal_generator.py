from __future__ import annotations

import random

from src.ast.first_order_logic import Literal
from src.generators import AstGenerator


class LiteralGenerator(AstGenerator):
    def __init__(self, negation_chance: float, atom_gen: AtomSignatureGenerator):
        self.negation_chance = negation_chance
        self.atom_gen = atom_gen

    def generate(self) -> Literal:
        # todo add negation prob
        return Literal(items=self.atom_gen.generate(), negated=random.random() < self.negation_chance)
