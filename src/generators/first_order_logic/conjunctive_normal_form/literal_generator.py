from __future__ import annotations

from src.ast.first_order_logic import Literal


class LiteralGenerator:
    def __init__(self, allow_positive: bool, allow_negated: bool, atom_gen: AtomGenerator):
        self.atom_gen = atom_gen
        self.allow_positive = allow_positive
        self.allow_negated = allow_negated

    def generate(self):
        assert self.allow_positive or self.allow_negated
        for allowed_atom in self.atom_gen.generate():
            if self.allow_negated:
                yield Literal(item=allowed_atom, negated=True)
            if self.allow_positive:
                yield Literal(item=allowed_atom, negated=False)
