from __future__ import annotations

from .ast_element import AstElement
from .term import Term


class Variable(Term, AstElement):
    def __init__(self, name: str):
        super().__init__(name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        return False
