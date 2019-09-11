from __future__ import annotations

from typing import Iterable

from .ast_element import AstElement
from .containers import TermContainer
from .term import Term


class Functor(Term, TermContainer, AstElement):
    def __init__(self, name: str, terms: Iterable[Term] = None, mutable=True):
        Term.__init__(self, name)
        TermContainer.__init__(self, additional_containers=[], items=terms, mutable=mutable)

    def __hash__(self):
        if self.is_mutable:
            return hash(self.name) + hash(len(self._items))
        else:
            return hash(self.name) + hash(self._items)

    def __eq__(self, other):
        if not isinstance(other, Functor):
            raise NotImplemented
        return self.name == other.name and len(self._items) == len(other._items) and \
               all(item == other_item for item, other_item in zip(self._items, other._items))

    def __str__(self):
        if len(list(self.items())) != 0:
            return f'{self.name}({", ".join(str(t) for t in self.items())})'
        else:
            return f'{self.name}'

    @property
    def arity(self):
        return len(self.items())

    @property
    def is_recursive(self):
        return any(isinstance(t, Functor) for t in self.items())

    @property
    def recursion_depth(self):
        if self.is_recursive:
            return max(f.recursion_depth + 1 for f in self.functors())
        else:
            return 0

    @property
    def is_constant(self):
        return len(self._items) == 0
