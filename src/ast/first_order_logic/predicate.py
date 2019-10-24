from __future__ import annotations

from typing import Iterable, Set, Type

from src.ast.containers import Container
from .folelement import FOLElement
from .term import Term


class Predicate(Container, FOLElement):
    def __init__(self, name: str, items: Iterable[Term] = None, *args, **kwargs):
        self.name = name
        super().__init__(items=items, *args, **kwargs)

    def __str__(self):
        if len(list(self.items(type=Term))) != 0:
            return f'{self.name}({", ".join(str(t) for t in self._items)})'
        else:
            return f'{self.name}'

    def __hash__(self):
        return Term.__hash__(self) ^ Container.__hash__(self)

    def __eq__(self, other):
        if isinstance(other, Predicate):
            return Term.__eq__(self, other) and Container.__eq__(self, other)
        raise NotImplementedError

    @property
    def arity(self):
        return len(self._items)

    @classmethod
    def contains(cls) -> Set[Type[FOLElement]]:
        from src.ast.first_order_logic import Functor, Variable
        return {Variable, Functor}
