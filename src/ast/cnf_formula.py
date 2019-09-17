from __future__ import annotations

from typing import List

from .ast_element import AstElement
from .cnf_clause import CNFClause
from .containers import CNFClauseContainer


class CNFFormula(CNFClauseContainer, AstElement):
    def __init__(self, clauses: List[CNFClause], mutable=True, related_placeholder: Placeholder = None):
        super().__init__(additional_containers=[], items=clauses, mutable=mutable)
        AstElement.__init__(self, related_placeholder=related_placeholder)

    def __str__(self):
        return '\n'.join(str(c) for c in self.clauses())

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if isinstance(other, CNFFormula):
            return super().__eq__(other)
        return False
