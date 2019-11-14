from __future__ import annotations

from typing import Set, Type

from ._temporal_logic_element import TemporalLogicElement
from .._containers import Container


class Formula(Container, TemporalLogicElement):
    """Propositional Temporal Logic"""

    @classmethod
    def contains(cls) -> Set[Type[TemporalLogicElement]]:
        from ._variable import Variable
        return {Formula, Variable}
