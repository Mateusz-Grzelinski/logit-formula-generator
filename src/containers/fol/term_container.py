from __future__ import annotations

from typing import overload, Tuple, Iterable

from .functor_container import FunctorContainer
from .variable_container import VariableContainer
from ...containers import MutableContainer


class TermContainer(VariableContainer, FunctorContainer, container_implementation=MutableContainer):
    @overload
    def terms(self, enum: bool = True) -> Iterable[Tuple[Container, int, Term]]:
        ...

    @overload
    def terms(self, enum: bool = False) -> Iterable[Term]:
        ...

    def terms(self, enum: bool = False):
        from src.ast.fol.term import Term
        if enum:
            return ((container, i, t) for container, i, t in self.items(enum=True) if isinstance(t, Term))
        else:
            return (t for t in self.items() if isinstance(t, Term))