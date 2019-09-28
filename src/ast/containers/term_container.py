from __future__ import annotations

from typing import overload, Tuple, Iterable

from src.container import MutableContainer
from .functor_container import FunctorContainer
from .variable_container import VariableContainer


class TermContainer(VariableContainer, FunctorContainer, container_implementation=MutableContainer):
    @overload
    def terms(self, enum: bool = True) -> Iterable[Tuple[Container, int, Term]]:
        ...

    @overload
    def terms(self, enum: bool = False) -> Iterable[Term]:
        ...

    @property
    def terms(self, enum: bool = False):
        from src.ast.term import Term
        if enum:
            return ((container, i, t) for container, i, t in self.items(enum=True) if isinstance(t, Term))
        else:
            return (t for t in self.items() if isinstance(t, Term))
