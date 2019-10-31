from __future__ import annotations

from src.ast.first_order_logic import Literal
from src.generators import AstGenerator


class LiteralSignatureGenerator(AstGenerator):
    def __init__(self, atom_gen: AtomGenerator):
        self.atom_gen = atom_gen

    def generate(self):
        for allowed_atom in self.atom_gen.generate():
            yield Literal(items=allowed_atom, negated=False)
