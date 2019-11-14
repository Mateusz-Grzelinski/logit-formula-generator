from __future__ import annotations

from typing import Iterable, Set, Type

from ._first_order_logic_element import FirstOrderLogicElement
from ._term import Term
from .._containers import Container


class Functor(Term, Container, FirstOrderLogicElement):

    def __init__(self, name: str, items: Iterable[Term] = None,
                 *args, **kwargs):
        super().__init__(name=name, items=items, *args, **kwargs)

    def __hash__(self):
        return Term.__hash__(self) ^ Container.__hash__(self)

    def __eq__(self, other):
        if isinstance(other, Functor):
            return Term.__eq__(self, other) and Container.__eq__(self, other)
        elif isinstance(other, FirstOrderLogicElement):
            return False
        raise NotImplementedError

    def __str__(self):
        if len(list(self._items)) != 0:
            return f'{self.name}({", ".join(str(t) for t in self._items)})'
        else:
            return f'{self.name}'

    @property
    def arity(self):
        return len(self._items)

    @property
    def is_recursive(self):
        return any(isinstance(t, Functor) for t in self.items())

    @property
    def recursion_depth(self):
        if self.is_recursive:
            return max(f.recursion_depth + 1 for f in self.items(type=Functor))
        else:
            return 0

    @property
    def is_constant(self):
        return len(self._items) == 0

    @classmethod
    def contains(cls) -> Set[Type[FirstOrderLogicElement]]:
        from src.ast.first_order_logic import Variable
        return {Functor, Variable}
