from __future__ import annotations

from typing import List

from .ast_element import AstElement
from .containers import TermContainer
from .term import Term


class Functor(Term, TermContainer, AstElement):
    def __init__(self, name: str, terms: List[Term] = None):
        Term.__init__(self, name)
        TermContainer.__init__(self, additional_containers=[], items=terms)

    def __hash__(self):
        return hash(self.name) + hash(tuple(self.items()))

    def __eq__(self, other):
        if not isinstance(other, Functor):
            raise NotImplemented
        return self.name == other.name and all(
            item == other_item for item, other_item in zip(self.items(), other.items()))

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
        return len(self.items()) == 0
