from __future__ import annotations

from typing import Iterable

from src.containers import ConstantLengthContainer
from src.containers.fol import CNFClauseContainer
from .cnf_clause import CNFClause
from .folelement import FolElement


class CNFFormula(CNFClauseContainer, FolElement, container_implementation=ConstantLengthContainer):
    def __init__(self, items: Iterable[CNFClause], related_placeholder: Placeholder = None, parent: CNFFormula = None,
                 scope: CNFFormula = None, *args, **kwargs):
        super().__init__(items=items, related_placeholder=related_placeholder, parent=parent, scope=scope, *args,
                         **kwargs)

    def __str__(self):
        return '\n'.join(str(c) for c in self.clauses())

    def __eq__(self, other):
        if isinstance(other, CNFFormula):
            return super().__eq__(other)
        raise NotImplementedError

    def update_scope(self):
        from src.ast.fol import CNFFormula
        parent = self.parent
        while parent is not None:
            if isinstance(parent, CNFFormula):
                self.scope = parent
                break
            parent = parent.parent
