from __future__ import annotations

from typing import List

from .containers import TermContainer
from .term import Term


class Functor(Term, TermContainer):
    def __init__(self, name: str,
                 terms: List[Term] = None):
        Term.__init__(self, name)
        TermContainer.__init__(self, additional_containers=[], items=terms)

    def __str__(self):
        if len(self.items) != 0:
            return f'{self.name}({", ".join(str(t) for t in self.items)})'
        else:
            return f'{self.name}'

    @property
    def arity(self):
        return len(self.items)

    @property
    def is_recursive(self):
        return any(isinstance(t, Functor) for t in self.items)

    @property
    def recursion_depth(self):
        if self.is_recursive:
            return max(f.recursion_depth + 1 for f in self.functors)
        else:
            return 0

    @property
    def is_constant(self):
        return len(self.items) == 0
