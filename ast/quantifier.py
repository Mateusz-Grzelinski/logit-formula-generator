from __future__ import annotations

from typing import List

from .atom import Atom
from .containers import QuantifierContainer
from .variable import Variable


class Quantifier(QuantifierContainer):
    """Stores first variables declared in this quantifier,
    and then formula?
    """

    def __init__(self, variables: List[Variable], atoms: List[Atom]):
        self.is_existential: bool = False
        self.is_universal: bool = False
        # todo
        super().__init__(items=variables + atoms)

    # def __str__(self):
    #     return '[' + ','.join(self.declared_variables.variables) + ']' + \
    #            str(self.atoms)
