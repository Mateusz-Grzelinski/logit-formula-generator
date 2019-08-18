from __future__ import annotations
from typing import List, Union

from ast.term import Term
from ast.variable import Variable
from containers.term_container import TermContainer


class Functor(Term, TermContainer):
    def __init__(self, name: str,
                 terms: List[Union[Variable, Functor]] = None):
        Term.__init__(self, name)
        TermContainer.__init__(self, additional_containers=[], items=terms)

    def __str__(self):
        if self.terms:
            return f'{self.name}({", ".join(str(t) for t in self.terms)})'
        else:
            return f'{self.name}'
