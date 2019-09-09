from __future__ import annotations

from typing import Iterable

from ast.containers import AtomContainer


class LiteralContainer(AtomContainer):

    @staticmethod
    def _item_type_check(obj):
        from ast.literal import Literal
        return isinstance(obj, Literal)

    def literals(self, enum: bool = False) -> Iterable[Literal]:
        from ast.literal import Literal
        if enum:
            return ((container, i, l) for container, i, l in self.items(enum=True) if isinstance(l, Literal))
        else:
            return (l for l in self.items() if isinstance(l, Literal))

    @property
    def number_of_literal_instances(self):
        return len(list(self.literals()))

    @property
    def number_of_literals(self):
        return len(set(self.literals()))
