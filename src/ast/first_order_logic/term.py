from __future__ import annotations

from abc import ABC

from .folelement import FolElement


class Term(ABC, FolElement):
    """Term is element of language

    """

    def __init__(self, name: str, parent: AstElement = None, scope: AstElement = None, *args, **kwargs):
        self.name = name
        super().__init__(parent=parent, scope=scope, *args, **kwargs)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Term):
            return self.name == other.name
        return False

    def __str__(self):
        return self.name

    def update_scope(self):
        from src.ast.first_order_logic import CNFFormula
        parent = self.parent
        while parent is not None:
            if isinstance(parent, CNFFormula):
                self.scope = parent
                break
            parent = parent.parent
