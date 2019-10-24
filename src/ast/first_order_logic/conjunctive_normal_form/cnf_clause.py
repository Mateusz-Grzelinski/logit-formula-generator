from __future__ import annotations

from collections.abc import Iterable
from typing import Set, Type

from src.ast.connectives import LogicalConnective
from src.ast.containers import Container
from src.ast.first_order_logic.folelement import FOLElement


class CNFClause(Container, FOLElement):
    connective = LogicalConnective.AND

    def __init__(self, items: Iterable[Literal] = None, *args, **kwagrs):
        super().__init__(items=items, *args, **kwagrs)

    def __str__(self):
        from src.ast.first_order_logic import Literal
        return 'cnf(' + '|'.join(str(l) for l in self.items(type=Literal)) + ').'

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if isinstance(other, CNFClause):
            return super().__eq__(other)
        raise NotImplementedError

    @property
    def length(self) -> int:
        return len(self._items)

    @property
    def is_unit(self) -> bool:
        return len(self._items) == 1

    @property
    def is_horn(self) -> bool:
        """A Horn clause is a clause (a disjunction of literals) with at most one positive, i.e. unnegated, literal"""
        from src.ast.first_order_logic import Literal
        positive_literals = 0
        for literal in self.items(type=Literal):
            if not literal.is_negated:
                positive_literals += 1
        return positive_literals <= 1

    @property
    def number_of_singleton_variables(self) -> int:
        from src.ast.first_order_logic import Variable
        variables = list(self.items(type=Variable))
        singleton_vars = set([x for x in variables if variables.count(x) == 1])
        return len(singleton_vars)

    @classmethod
    def contains(cls) -> Set[Type[FOLElement]]:
        from src.ast.first_order_logic import Literal
        return {Literal}
