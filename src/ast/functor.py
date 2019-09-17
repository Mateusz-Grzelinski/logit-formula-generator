from __future__ import annotations

from typing import Iterable

from .ast_element import AstElement
from .containers import TermContainer
from .term import Term


class Functor(Term, TermContainer, AstElement):
    def __init__(self, name: str, terms: Iterable[Term] = None, mutable=True,
                 related_placeholder: FunctorPlaceholder = None):
        Term.__init__(self, name)
        TermContainer.__init__(self, additional_containers=[], items=terms, mutable=mutable)
        AstElement.__init__(self, related_placeholder=related_placeholder)

    def __hash__(self):
        return hash(self.name) + hash(len(self._items))

    def __eq__(self, other):
        if isinstance(other, Functor):
            return self.name == other.name and len(self._items) == len(other._items)
        return False

    def __str__(self):
        if len(list(self._items)) != 0:
            return f'{self.name}({", ".join(str(t) for t in self._items)})'
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
