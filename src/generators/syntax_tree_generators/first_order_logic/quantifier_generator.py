from __future__ import annotations

from typing import Generator, Any

import src.syntax_tree.first_order_logic as fol
from src.generators import SyntaxTreeGenerator


class QuantifierGenerator(SyntaxTreeGenerator):
    def __init__(self, atom_gen: AtomGenerator, number_of_atoms: int):
        self.number_of_atoms = number_of_atoms

    def generate(self) -> Generator[fol.Quantifier, Any, Any]:
        fol.Quantifier(children=[])
        fol.FirstOrderLogicFormula(children=[])
