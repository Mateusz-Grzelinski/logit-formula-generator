from __future__ import annotations
from typing import List

from containers.container import Container


class FunctorContainer(Container):
    @staticmethod
    def _type_check(obj):
        from ast.functor import Functor
        return isinstance(obj, Functor)

    @property
    def functors(self):
        from ast.functor import Functor
        return (f for f in self._items if isinstance(f, Functor))

    @property
    def number_of_functors(self):
        return len(set(self.functors)) + \
               sum(len(set(f_cont.functors)) for f_cont in self._other_containers if isinstance(f_cont,FunctorContainer))
