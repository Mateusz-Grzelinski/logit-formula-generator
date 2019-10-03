from __future__ import annotations

from typing import Iterable

from src.containers import ImmutableContainer
from src.containers.fol import TermContainer
from .folelement import FolElement
from .term import Term


class Predicate(TermContainer, FolElement, container_implementation=ImmutableContainer):
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
        return Term.__hash__(self) ^ TermContainer.__hash__(self)

    def __eq__(self, other):
        if isinstance(other, Predicate):
            return Term.__eq__(self, other) and TermContainer.__eq__(self, other)
        raise NotImplementedError

    def update_scope(self):
        from src.ast.first_order_logic import CNFFormula
        parent = self.parent
        while parent is not None:
            if isinstance(parent, CNFFormula):
                self.scope = parent
                break
            parent = parent.parent
