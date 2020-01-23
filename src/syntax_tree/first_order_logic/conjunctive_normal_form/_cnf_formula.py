from __future__ import annotations

from typing import Iterable

from ._cnf_clause import CNFClause
from .._formula import FOLFormula
from ..info.cnf_formula_info import CNFFormulaInfo
from ...connectives import LogicalConnective
from ...syntax_tree import FirstOrderLogicNode


class CNFFOLFormula(FOLFormula):
    def __init__(self, children: Iterable[CNFClause]):
        super().__init__(children=children, binary_logical_connective=LogicalConnective.AND)

    def __str__(self):
        return '\n'.join(str(c) for c in self)

    def __eq__(self, other):
        if isinstance(other, CNFFOLFormula):
            return super().__eq__(other)
        elif isinstance(other, FirstOrderLogicNode):
            return False
        raise NotImplementedError

    def get_info(self) -> CNFFormulaInfo:
        from src.syntax_tree.first_order_logic.visitors.cnf_formula_visitor import CNFFormulaVisitor
        walker = CNFFormulaVisitor()
        self._accept(walker)
        return walker.info

    def equivalent(self, formula: CNFFOLFormula):
        """Compare 2 clauses but do not take into account order of literals"""
        for item in self:
            if item not in formula:
                return False
        return True

    def equivalent_in(self, formulas: Iterable[CNFFOLFormula]):
        for cnf_formulas in formulas:
            if self.equivalent(cnf_formulas):
                return True
        return False
