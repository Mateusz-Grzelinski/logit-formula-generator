from __future__ import annotations

from typing import Iterable

from src.ast.first_order_logic.conjunctive_normal_form.containers.cnf_clause_container import CNFClauseContainer
from src.ast.first_order_logic.folelement import FolElement
from .cnf_clause import CNFClause


class CNFFormula(CNFClauseContainer, FolElement):
    def __init__(self, items: Iterable[CNFClause], parent: CNFFormula = None, scope: CNFFormula = None, *args,
                 **kwargs):
        super().__init__(items=items, parent=parent, scope=scope, *args, **kwargs)

    def __str__(self):
        return '\n'.join(str(c) for c in self.clauses())

    def __eq__(self, other):
        if isinstance(other, CNFFormula):
            return super().__eq__(other)
        raise NotImplementedError

    def update_scope(self):
        from src.ast.first_order_logic import CNFFormula
        parent = self.parent
        while parent is not None:
            if isinstance(parent, CNFFormula):
                self.scope = parent
                break
            parent = parent.parent
