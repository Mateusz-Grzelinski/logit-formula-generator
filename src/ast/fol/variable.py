from __future__ import annotations

from src.ast.ast_element import AstElement
from .term import Term


class Variable(Term, AstElement):
    def __init__(self, name: str, related_placeholder: VariablePlaceholder = None):
        super().__init__(name)
        AstElement.__init__(self, related_placeholder=related_placeholder)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        return False
