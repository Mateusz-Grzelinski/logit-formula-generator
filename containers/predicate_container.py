from __future__ import annotations
from typing import List, Generator

from containers.container import Container


class PredicateContainer(Container):
    @staticmethod
    def _type_check(obj):
        from ast.predicate import Predicate
        return isinstance(obj, Predicate)

    # def __init__(self, predicates: List[Predicate] = None):
    #     super().__init__(predicates)

    @property
    def predicates(self) -> Generator:
        from ast.predicate import Predicate
        return (p for p in self._items if isinstance(p, Predicate))

    @property
    def number_of_predicates(self):
        return len(list(self.predicates)) + \
               sum(len(list(p_cont.predicates)) for p_cont in self._other_containers if
                   isinstance(p_cont, PredicateContainer))
