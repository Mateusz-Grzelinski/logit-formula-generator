from __future__ import annotations

from typing import Iterable, Set, Type, Any

from src.ast import LogicalConnective
from ._atom import Atom
from ._quantifier import Quantifier
from .._ast_element import AstElement
from .._containers import Container


class Formula(Container, AstElement):
    def __init__(self, items: Iterable[Atom, Quantifier, Formula], logical_connective: LogicalConnective, *args,
                 **kwargs):
        super().__init__(items, *args, **kwargs)
        self.logical_connective = logical_connective

    @classmethod
    def contains(cls) -> Set[Type[Any]]:
        return {Atom, Quantifier}

    def __str__(self):
        if len(self) == 1:
            return ''.join(str(i) for i in self.unary_connective if i.connective != None) + str(self[0])
        else:
            return ''.join(str(i) for i in self.unary_connective if i.connective != None) + str(self[0]) + ' ' + str(
                self.logical_connective.value) + ' ' + str(self[1])
