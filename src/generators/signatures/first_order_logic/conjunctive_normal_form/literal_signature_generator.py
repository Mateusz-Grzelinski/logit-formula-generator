from __future__ import annotations

from src.ast.first_order_logic import Literal


class LiteralSignatureGenerator:
    def __init__(self, atom_gen: AtomGenerator):
        self.atom_gen = atom_gen

    def generate(self):
        for allowed_atom in self.atom_gen.generate():
            yield Literal(item=allowed_atom, negated=False)
