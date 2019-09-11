from typing import Iterable

from .ast_element import AstElement
from .containers import TermContainer
from .term import Term


class Predicate(TermContainer, AstElement):
    def __init__(self, name: str, terms: Iterable[Term] = None, mutable=True):
        self.name = name
        super().__init__(additional_containers=[], items=terms, mutable=mutable)

    def __str__(self):
        if len(list(self.terms)) != 0:
            return f'{self.name}({", ".join(str(t) for t in self.terms)})'
        else:
            return f'{self.name}'

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self):
        return hash(self.name) + hash(len(self._items))

    def __eq__(self, other):
        if isinstance(other, Predicate):
            return self.name == other.name and len(self._items) == len(other._items)
        return False
