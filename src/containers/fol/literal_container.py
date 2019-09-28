from __future__ import annotations

from typing import Iterable, overload, Tuple

from .atom_container import AtomContainer
from ...containers import MutableContainer


class LiteralContainer(AtomContainer, container_implementation=MutableContainer):
    def __init__(self, items: Iterable[Literal], *args, **kwargs):
        super().__init__(items=items, *args, **kwargs)

    @overload
    def literals(self, enum: bool = True) -> Iterable[Tuple[Container, int, Literal]]:
        ...

    @overload
    def literals(self, enum: bool = False) -> Iterable[Literal]:
        ...

    def literals(self, enum: bool = False) -> Iterable:
        from src.ast.fol.literal import Literal
        if enum:
            return ((container, i, l) for container, i, l in self.items(enum=True) if isinstance(l, Literal))
        else:
            return (l for l in self.items() if isinstance(l, Literal))

    @property
    def number_of_literal_instances(self):
        return len(list(self.literals()))

    @property
    def number_of_literals(self):
        return len(set(self.literals()))
