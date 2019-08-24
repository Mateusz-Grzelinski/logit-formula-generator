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
        if self.terms:
            return f'{self.name}({", ".join(str(t) for t in self.terms)})'
        else:
            return f'{self.name}'

    def arity(self):
        return len(self.items)

    def is_recursive(self):
        return any(isinstance(t, Functor) for t in self.items)

    def is_constant(self):
        return len(self.items) == 0
