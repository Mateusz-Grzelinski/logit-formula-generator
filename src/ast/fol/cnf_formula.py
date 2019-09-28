from __future__ import annotations

from typing import Iterable

from src.ast.ast_element import AstElement
from src.containers import ConstantLengthContainer
from src.containers.fol import CNFClauseContainer
from .cnf_clause import CNFClause


class CNFFormula(CNFClauseContainer, AstElement, container_implementation=ConstantLengthContainer):
    def __init__(self, items: Iterable[CNFClause], related_placeholder: Placeholder = None, *args, **kwargs):
        super().__init__(items=items, related_placeholder=related_placeholder, *args, **kwargs)

    def __str__(self):
        return '\n'.join(str(c) for c in self.clauses())

    def __eq__(self, other):
        if isinstance(other, CNFFormula):
            return super().__eq__(other)
        raise NotImplementedError
