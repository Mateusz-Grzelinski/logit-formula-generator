from typing import Generator

from containers.predicate_container import PredicateContainer
from containers.term_container import TermContainer


class AtomContainer(TermContainer, PredicateContainer):

    @staticmethod
    def _type_check(obj):
        from ast.atom import Atom
        return isinstance(obj, Atom)

    def atoms(self) -> Generator:
        from ast.atom import Atom
        return (a for a in self._items if isinstance(a, Atom))
