from __future__ import annotations

from typing import List

from ast.containers import TermContainer
from ast.term import Term


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
