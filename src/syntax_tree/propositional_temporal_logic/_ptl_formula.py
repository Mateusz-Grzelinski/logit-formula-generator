from __future__ import annotations

from typing import Set, Type, MutableSequence

from src.syntax_tree.propositional_temporal_logic.info.cnf_ptl_formula_info import \
    ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo
from ..syntax_tree import ChildrenType, TemporalLogicNode


class PTLFormula(TemporalLogicNode):
    """Propositional Temporal Logic"""

    def __init__(self, children: MutableSequence[ChildrenType], logical_connective: ConnectiveProperties, *args,
                 **kwargs):
        super().__init__(children, *args, **kwargs)
        self.logical_connective = logical_connective

    @classmethod
    def contains(cls) -> Set[Type[TemporalLogicNode]]:
        from ._variable import Variable
        return {PTLFormula, Variable}

    def get_info(self) -> ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo:
        from src.syntax_tree.propositional_temporal_logic.visitors.cnf_ptl_formula_visitor import CNFPTLFormulaVisitor
        walker = CNFPTLFormulaVisitor()
        self._accept(walker)
        return walker.info

    def __str__(self):
        # this is hack to convert and to & and or to |
        from src.syntax_tree import LogicalConnective

        def convert_to_inkresat_fomat(connective: LogicalConnective):
            if connective == LogicalConnective.AND:
                return '&'
            if connective == LogicalConnective.OR:
                return '|'

        unary_connectives = ''.join(
            convert_to_inkresat_fomat(i.connective) for i in self.unary_connectives if i.connective is not None)
        formula = (str(i) for i in self)
        return unary_connectives + convert_to_inkresat_fomat(self.logical_connective.connective).join(formula)
