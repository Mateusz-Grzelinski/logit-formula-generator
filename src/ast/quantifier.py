from __future__ import annotations

from typing import List

from .ast_element import AstElement
from .atom import Atom
from .containers import QuantifierContainer
from .variable import Variable


class Quantifier(QuantifierContainer, AstElement):
    """Stores first variables declared in this quantifier,
    and then formula?
    """

    def __init__(self, variables: List[Variable], atoms: List[Atom], related_placeholder: QuantifierPlaceholder = None):
        self.is_existential: bool = False
        self.is_universal: bool = False
        # todo
        super().__init__(items=variables + atoms)
        AstElement.__init__(self, related_placeholder=related_placeholder)

    # def __str__(self):
    #     return '[' + ','.join(self.declared_variables.variables) + ']' + \
    #            str(self.atoms)
