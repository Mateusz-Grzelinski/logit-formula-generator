from __future__ import annotations

from statistics import mean
from typing import Iterable, overload, Tuple, Set, Type

from .literal_container import LiteralContainer


class CNFClauseContainer(LiteralContainer):
    def __init__(self, items: Iterable[CNFClause], *args, **kwargs):
        super().__init__(items=items, *args, **kwargs)
        assert len(self._items) != 0

    @classmethod
    def contains(cls) -> Set[Type]:
        from src.ast.first_order_logic import CNFClause
        return {CNFClause}

    @overload
    def clauses(self, enum: bool = True) -> Iterable[Tuple[Container, int, CNFClause]]:
        ...

    @overload
    def clauses(self, enum: bool = False) -> Iterable[CNFClause]:
        ...

    def clauses(self, enum: bool = False) -> Iterable[CNFClause]:
        from src.ast.first_order_logic.conjunctive_normal_form.cnf_clause import CNFClause
        if enum:
            return ((container, i, c) for container, i, c in self.items(enum=True) if isinstance(c, CNFClause))
        else:
            return (c for c in self.items() if isinstance(c, CNFClause))

    @property
    def number_of_clause_instances(self) -> int:
        return len(self._items)

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
