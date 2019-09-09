from __future__ import annotations

from typing import Iterable

from .literal_container import LiteralContainer


class CNFClauseContainer(LiteralContainer):
    @staticmethod
    def _item_type_check(obj):
        from ast.cnf_clause import CNFClause
        return isinstance(obj, CNFClause)

    def clauses(self, enum: bool = False) -> Iterable[CNFClause]:
        from ast.cnf_clause import CNFClause
        if enum:
            return ((container, i, c) for container, i, c in self.items(enum=True) if isinstance(c, CNFClause))
        else:
            return (c for c in self.items() if isinstance(c, CNFClause))

    @property
    def number_of_clauses(self) -> int:
        return len(list(self.clauses()))
