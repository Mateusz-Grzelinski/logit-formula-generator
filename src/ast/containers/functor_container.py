from __future__ import annotations

from src.common.container import Container


class FunctorContainer(Container):
    @staticmethod
    def _item_type_check(obj):
        from src.ast import Functor
        return isinstance(obj, Functor)

    def functors(self, enum: bool = False):
        from src.ast import Functor
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
