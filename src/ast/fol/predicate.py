from __future__ import annotations

from typing import Iterable

from src.containers import ConstantLengthContainer
from src.containers.fol import TermContainer
from .folelement import FolElement
from .term import Term


class Predicate(TermContainer, FolElement, container_implementation=ConstantLengthContainer):
    def __init__(self, name: str, items: Iterable[Term] = None, related_placeholder: PredicatePlaceholder = None,
                 parent: CNFFormula = None, scope: CNFFormula = None, *args, **kwargs):
        self.name = name
        super().__init__(items=items, related_placeholder=related_placeholder, parent=parent, scope=scope,
                         *args, **kwargs)

    def __str__(self):
        if len(list(self.terms())) != 0:
            return f'{self.name}({", ".join(str(t) for t in self.terms())})'
        else:
            return f'{self.name}'

    def __hash__(self):
        return hash(self.name) + super().__hash__()

    def __eq__(self, other):
        if isinstance(other, Predicate):
            return self.name == other.name and super().__eq__(other)
        raise NotImplementedError

    def update_scope(self):
        from src.ast.fol import CNFFormula
        parent = self.parent
        while parent is not None:
            if isinstance(parent, CNFFormula):
                self.scope = parent
                break
            parent = parent.parent
