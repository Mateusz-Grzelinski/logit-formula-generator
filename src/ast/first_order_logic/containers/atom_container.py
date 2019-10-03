from __future__ import annotations

from typing import overload, Iterable, Tuple, Set, Type

from .predicate_container import PredicateContainer
from .term_container import TermContainer


class AtomContainer(TermContainer, PredicateContainer):
    def __init__(self, items: Iterable[Atom], *args, **kwargs):
        super().__init__(items=items, *args, **kwargs)

    @classmethod
    def contains(cls) -> Set[Type]:
        from src.ast.first_order_logic import Atom
        return {Atom}

    @overload
    def atoms(self, enum: bool = True) -> Iterable[Tuple[Container, int, Atom]]:
        ...

    @overload
    def atoms(self, enum: bool = False) -> Iterable[Atom]:
        ...

    def atoms(self, enum: bool = False) -> Iterable:
        from src.ast.first_order_logic.atom import Atom
        if enum:
            return ((container, i, a) for container, i, a in self.items(enum=True) if isinstance(a, Atom))
        else:
            return (a for a in self.items() if isinstance(a, Atom))

    @property
    def number_of_atoms(self):
        # todo fix hash
        return len(set(self.atoms()))

    @property
    def number_of_atom_instances(self):
        return len(list(self.atoms()))
