from __future__ import annotations

from typing import Set, Type, MutableSequence

from src.ast._containers import ItemType
from src.ast.propositional_temporal_logic.info.cnf_ptl_formula_info import CNFPTLFormulaInfo
from ._temporal_logic_element import TemporalLogicElement
from .._containers import Container


class PTLFormula(Container, TemporalLogicElement):
    """Propositional Temporal Logic"""

    def __init__(self, items: MutableSequence[ItemType], logical_connective: ConnectiveProperties, *args,
                 **kwargs):
        super().__init__(items, *args, **kwargs)
        self.logical_connective = logical_connective

    @classmethod
    def contains(cls) -> Set[Type[TemporalLogicElement]]:
        from ._variable import Variable
        return {PTLFormula, Variable}

    def get_info(self) -> CNFPTLFormulaInfo:
        from src.ast.propositional_temporal_logic.visitors.cnf_ptl_formula_visitor import CNFPTLFormulaVisitor
        walker = CNFPTLFormulaVisitor()
        self._accept(walker)
        return walker.info

    def __str__(self):
        unary_connectives = ''.join(i.connective.value for i in self.unary_connectives if i.connective is not None)
        formula = (str(i) for i in self)
        return unary_connectives + str(self.logical_connective.connective.value).join(formula)
