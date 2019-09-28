from __future__ import annotations

from abc import ABC

from src.ast.ast_element import AstElement


class Term(ABC, AstElement):
    """Term is element of language

    """

    def __init__(self, name: str, related_placeholder: Placeholder = None, parent: AstElement = None,
                 scope: AstElement = None, *args, **kwargs):
        self.name = name
        super().__init__(related_placeholder=related_placeholder, parent=parent, scope=scope, *args,
                         **kwargs)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Term):
            return self.name == other.name
        return False

    def __str__(self):
        return self.name

    def update_scope(self):
        from src.ast.fol import CNFFormula
        parent = self.parent
        while parent is not None:
            if isinstance(parent, CNFFormula):
                self.scope = parent
                break
            parent = parent.parent
