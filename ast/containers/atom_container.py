from __future__ import annotations

from typing import Generator

from .predicate_container import PredicateContainer
from .term_container import TermContainer


class AtomContainer(TermContainer, PredicateContainer):

    @staticmethod
    def _item_type_check(obj):
        from ast.atom import Atom
        return isinstance(obj, Atom)

    def atoms(self, enum: bool = False) -> Generator:
        from ast.atom import Atom
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
