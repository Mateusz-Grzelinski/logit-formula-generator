from __future__ import annotations

from statistics import mean
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

    @property
    def number_of_singleton_variables(self) -> int:
        return sum(clause.number_of_singleton_variables for clause in self.clauses())

    @property
    def number_of_unit_clauses(self):
        return len(list(c for c in self.clauses() if c.is_unit))

    @property
    def max_clause_size(self):
        return max(clause.length for clause in self.clauses())

    @property
    def average_clause_size(self):
        return mean(clause.length for clause in self.clauses())

    @property
    def number_of_variables(self) -> int:
        return sum(clause.number_of_variables for clause in self.clauses())

    @property
    def number_of_variable_instances(self) -> int:
        return sum(clause.number_of_variable_instances for clause in self.clauses())
