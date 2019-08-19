from typing import Generator

from ast.containers import PredicateContainer
from ast.containers import TermContainer


class AtomContainer(TermContainer, PredicateContainer):

    @staticmethod
    def _type_check(obj):
        from ast.atom import Atom
        return isinstance(obj, Atom)

    def atoms(self) -> Generator:
        from ast.atom import Atom
        return (a for a in self._items if isinstance(a, Atom))
