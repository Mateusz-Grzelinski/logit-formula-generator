from __future__ import annotations

from typing import Set, Type, MutableSequence

from src.ast._containers import ItemType
from ._temporal_logic_element import TemporalLogicElement
from .._containers import Container


class Formula(Container, TemporalLogicElement):
    """Propositional Temporal Logic"""

    def __init__(self, items: MutableSequence[ItemType], logical_connective: ConnectiveProperties, *args,
                 **kwargs):
        super().__init__(items, *args, **kwargs)
        self.logical_connective = logical_connective

    @classmethod
    def contains(cls) -> Set[Type[TemporalLogicElement]]:
        from ._variable import Variable
        return {Formula, Variable}

    def __str__(self):
        unary_connectives = ''.join(i.connective.value for i in self.unary_connective if i.connective is not None)
        formula = (str(i) for i in self)
        return unary_connectives + str(self.logical_connective.connective.value).join(formula)
