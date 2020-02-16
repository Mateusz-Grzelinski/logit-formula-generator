from __future__ import annotations

from typing import Iterable

from src.data_model.cnf_formula_info import CNFFormulaInfo
from src.syntax_tree.first_order_logic.visitors.cnf_formula_info_collector import CNFFormulaInfoCollector
from .._fol_formula import FirstOrderLogicFormula
from ..conjunctive_normal_form._cnf_clause import CNFClause
from ...connectives import LogicalConnective
from ...syntax_tree import FirstOrderLogicNode


class CNFFirstOrderLogicFormula(FirstOrderLogicFormula):
    """todo remove"""
    def __init__(self, children: Iterable[CNFClause]):
        super().__init__(children=children, binary_logical_connective=LogicalConnective.AND)

    def __str__(self):
        return '\n'.join(str(c) for c in self)

    def __eq__(self, other):
        if isinstance(other, CNFFirstOrderLogicFormula):
            return super().__eq__(other)
        elif isinstance(other, FirstOrderLogicNode):
            return False
        raise NotImplementedError

    def get_formula_info(self) -> CNFFormulaInfo:
        walker = CNFFormulaInfoCollector()
        self._accept(walker)
        return walker.info

    def get_tptp_header(self, info: CNFFormulaInfo) -> str:
        # todo implement
        raise NotImplementedError

    def equivalent(self, formula: CNFFirstOrderLogicFormula):
        """Compare 2 clauses but do not take into account order of literals"""
        for item in self:
            if item not in formula:
                return False
        return True

    def equivalent_in(self, formulas: Iterable[CNFFirstOrderLogicFormula]):
        for cnf_formulas in formulas:
            if self.equivalent(cnf_formulas):
                return True
        return False

