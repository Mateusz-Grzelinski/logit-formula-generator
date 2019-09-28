from __future__ import annotations

from src.ast.ast_element import AstElement
from .cnf_clause import CNFClause
from .term import Term


class Variable(Term, AstElement):
    def __init__(self, name: str, related_placeholder: VariablePlaceholder = None, parent: AstElement = None,
                 scope: CNFClause = None, *args, **kwargs):
        super().__init__(name=name, related_placeholder=related_placeholder, parent=parent, scope=scope)

    def __hash__(self):
        if self.scope:
            return hash(self.name) + hash(self.scope)
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        return False

    def update_scope(self):
        parent = self.parent
        while parent is not None:
            if isinstance(parent, CNFClause):
                self.scope = parent
                break
            parent = parent.parent
