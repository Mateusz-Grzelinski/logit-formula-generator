from __future__ import annotations

from typing import overload, Tuple, Iterable

from ...containers import Container, MutableContainer


class FunctorContainer(Container, container_implementation=MutableContainer):
    def __init__(self, items: Iterable[Functor], *args, **kwargs):
        super().__init__(items=items, *args, **kwargs)

    @overload
    def functors(self, enum: bool = True) -> Iterable[Tuple[Container, int, Functor]]:
        ...

    @overload
    def functors(self, enum: bool = False) -> Iterable[Functor]:
        ...

    def functors(self, enum: bool = False):
        from src.ast.fol import Functor
        if enum:
            return ((container, i, f) for container, i, f in self.items(enum=True) if isinstance(f, Functor))
        else:
            return (f for f in self.items() if isinstance(f, Functor))

    @property
    def number_of_functors(self):
        return len(set(self.functors()))

    @property
    def number_of_functor_instances(self):
        return len(list(self.functors()))

    @property
    def number_of_constant_functors(self):
        return len(set(f for f in self.functors() if f.is_constant))

    @property
    def number_of_constant_functors_instances(self):
        return len(list(f for f in self.functors() if f.is_constant))

    @property
    def max_recursion_depth(self):
        if self.number_of_functors != 0:
            return max(f.recursion_depth for f in self.functors())
        else:
            return 0
