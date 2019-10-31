from __future__ import annotations

from typing import Set, Type

from src.ast._containers import Container
from src.ast.temporal_logic.tl_element import TLElement


class TLFormula(Container, TLElement):
    """Propositional Temporal Logic"""

    @classmethod
    def contains(cls) -> Set[Type[TLElement]]:
        from src.ast.temporal_logic import PropositionalVariable
        return {TLFormula, PropositionalVariable}
