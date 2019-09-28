from __future__ import annotations

from typing import Iterable

from src.ast.ast_element import AstElement
from src.containers import ConstantLengthContainer
from src.containers.fol import TermContainer
from .term import Term


class Predicate(TermContainer, AstElement, container_implementation=ConstantLengthContainer):
    def __init__(self, name: str, items: Iterable[Term] = None, related_placeholder: PredicatePlaceholder = None, *args,
                 **kwargs):
        super().__init__(name=name, items=items, related_placeholder=related_placeholder, *args, **kwargs)
        self.name = name

    def __str__(self):
        if len(list(self.terms())) != 0:
            return f'{self.name}({", ".join(str(t) for t in self.terms())})'
        else:
            return f'{self.name}'

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self):
        return hash(self.name) + super().__hash__()

    def __eq__(self, other):
        if isinstance(other, Predicate):
            return self.name == other.name and super().__eq__(other)
        raise NotImplementedError
