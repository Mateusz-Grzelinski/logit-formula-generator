from __future__ import annotations

from typing import Iterable

from src.syntax_tree import ConnectiveProperties
from ._atom import Atom
from ._quantifier import Quantifier
from ..syntax_tree import SyntaxTreeNode


class FOLFormula(SyntaxTreeNode):
    def __init__(self, children: Iterable[Atom, Quantifier, FOLFormula],
                 binary_logical_connective: ConnectiveProperties = None,
                 unary_connective: Iterable[ConnectiveProperties] = None):
        super().__init__(children)
        self.unary_connective = list(unary_connective) if unary_connective else []
        self.logical_connective = binary_logical_connective

    def __str__(self):
        unary_connectives = ' '.join(str(i) for i in self.unary_connective)
        return unary_connectives + self.logical_connective.sign.join(str(i) for i in self)
