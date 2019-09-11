from __future__ import annotations

from typing import Generator

from common.container import Container


class PredicateContainer(Container):
    @staticmethod
    def _item_type_check(obj):
        from ast.predicate import Predicate
        return isinstance(obj, Predicate)

    def predicates(self, enum: bool = False) -> Generator:
        from ast.predicate import Predicate
        if enum:
            return ((container, i, p) for container, i, p in self.items(enum=True) if isinstance(p, Predicate))
        else:
            return (p for p in self.items() if isinstance(p, Predicate))

    @property
    def number_of_predicates(self):
        return len(set(self.predicates()))

    @property
    def number_of_predicate_instances(self):
        return len(list(self.predicates()))
