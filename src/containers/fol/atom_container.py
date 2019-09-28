from __future__ import annotations

from typing import overload, Iterable, Tuple

from .predicate_container import PredicateContainer
from .term_container import TermContainer
from ...containers import MutableContainer


class AtomContainer(TermContainer, PredicateContainer, container_implementation=MutableContainer):
    @overload
    def atoms(self, enum: bool = True) -> Iterable[Tuple[Container, int, Atom]]:
        ...

    @overload
    def atoms(self, enum: bool = False) -> Iterable[Atom]:
        ...

    def atoms(self, enum: bool = False) -> Iterable:
        from src.ast.fol.atom import Atom
        if enum:
            return ((container, i, a) for container, i, a in self.items(enum=True) if isinstance(a, Atom))
        else:
            return (a for a in self.items() if isinstance(a, Atom))

    @property
    def number_of_atoms(self):
        return len(set(self.atoms()))

    @property
    def number_of_atom_instances(self):
        return len(list(self.atoms()))
