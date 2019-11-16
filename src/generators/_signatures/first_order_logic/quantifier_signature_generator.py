from __future__ import annotations

from typing import Generator, Any

import src.ast.first_order_logic as fol
from src.generators import AstGenerator


class QuantifierSignatureGenerator(AstGenerator):
    def __init__(self, atom_gen: AtomSignatureGenereator, number_of_atoms: int):
        self.number_of_atoms = number_of_atoms

    def generate(self) -> Generator[fol.Quantifier, Any, Any]:
        fol.Quantifier(items=[])
        fol.Formula(items=[])
