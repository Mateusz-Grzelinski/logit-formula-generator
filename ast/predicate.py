from typing import List

from .ast_element import AstElement
from .containers import TermContainer
from .term import Term


class Predicate(TermContainer, AstElement):
    def __init__(self, name: str, terms: List[Term] = None):
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
