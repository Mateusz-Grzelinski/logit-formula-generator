from typing import List, Union

from ast.containers import TermContainer
from ast.functor import Functor
from ast.variable import Variable


class Predicate(TermContainer):
    def __init__(self, name: str, terms: List[Union[Variable, Functor]] = None):
        self.name = name
        super().__init__(additional_containers=[], items=terms)

    def __str__(self):
        if self.terms:
            return f'{self.name}({", ".join(str(t) for t in self.terms)})'
        else:
            return f'{self.name}'

    def __repr__(self) -> str:
        return str(self)

    # arguments: List[Term]
