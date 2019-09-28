from __future__ import annotations

from typing import Generator, overload, Iterable, Tuple

from ...containers import Container, MutableContainer


class PredicateContainer(Container, container_implementation=MutableContainer):
    @overload
    def predicates(self, enum: bool = True) -> Iterable[Tuple[Container, int, Predicate]]:
        ...

    @overload
    def predicates(self, enum: bool = False) -> Iterable[Predicate]:
        ...

    def predicates(self, enum: bool = False) -> Generator:
        from src.ast.fol.predicate import Predicate
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
