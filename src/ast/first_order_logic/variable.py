from __future__ import annotations

from src.ast.ast_element import AstElement
from src.ast.first_order_logic.conjunctive_normal_form.cnf_clause import CNFClause
from .folelement import FolElement
from .term import Term


class Variable(Term, FolElement):
    def __init__(self, name: str, related_placeholder: VariablePlaceholder = None, parent: AstElement = None,
                 scope: CNFClause = None, *args, **kwargs):
        super().__init__(name=name, related_placeholder=related_placeholder, parent=parent, scope=scope)

    def __hash__(self):
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
