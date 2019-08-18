from __future__ import annotations

from typing import List

from ast.atom import Atom
from ast.variable import Variable
from containers.atom_container import AtomContainer
from containers.predicate_container import PredicateContainer
from containers.quantifier_container import QuantifierContainer
from containers.variable_container import VariableContainer


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
