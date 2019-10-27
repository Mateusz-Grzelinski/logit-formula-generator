from __future__ import annotations

from typing import Set, Type

from src.ast.connectives import LogicalConnective
from src.ast.containers import Container
from src.ast.first_order_logic.folelement import FOLElement


class Literal(Container, FOLElement):
    def __init__(self, items: Atom, negated: bool, *args, **kwargs):
        self.is_negated = negated
        unary_connective = LogicalConnective.NOT if negated else None
        super().__init__(items=[items], unary_connectives=[unary_connective], *args, **kwargs)

    def __hash__(self):
        return hash(self.is_negated) ^ Container.__hash__(self)

    def __eq__(self, other):
        if isinstance(other, Literal):
            return self.is_negated == other.is_negated and super().__eq__(other)
        return False

    def __str__(self):
        if self.is_negated:
            return '~' + str(self.atom)
        return str(self.atom)

    @property
    def atom(self):
        assert len(self._items) == 1, 'literal can have only one atom'
        return self._items[0]

    @classmethod
    def contains(cls) -> Set[Type[FOLElement]]:
        from src.ast.first_order_logic.atom import Atom
        return {Atom}
