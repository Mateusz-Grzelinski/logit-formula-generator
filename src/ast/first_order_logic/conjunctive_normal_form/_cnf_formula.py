from __future__ import annotations

from typing import Iterable, Set, Type

from src.ast.first_order_logic.visitors._cnf_formula_info import CNFFormulaInfo
from ._cnf_clause import CNFClause
from .._first_order_logic_element import FirstOrderLogicElement
from ..._containers import Container


class CNFFormula(Container, FirstOrderLogicElement):
    def __init__(self, items: Iterable[CNFClause], *args,
                 **kwargs):
        super().__init__(items=items, *args, **kwargs)

    def __str__(self):
        return '\n'.join(str(c) for c in self)

    def __eq__(self, other):
        if isinstance(other, CNFFormula):
            return super().__eq__(other)
        elif isinstance(other, FirstOrderLogicElement):
            return False
        raise NotImplementedError

    def get_info(self) -> CNFFormulaInfo:
        from src.ast.first_order_logic.conjunctive_normal_form._cnf_formula_visitor import CNFFormulaVisitor
        walker = CNFFormulaVisitor()
        self._accept(walker)
        return walker.info

    @classmethod
    def contains(cls) -> Set[Type[FirstOrderLogicElement]]:
        from ._cnf_clause import CNFClause
        return {CNFClause}

    def equivalent(self, formula: CNFFormula):
        """Compare 2 clauses but do not take into account order of literals"""
        for item in self._items:
            if item not in formula:
                return False
        return True

    def equivalent_in(self, formulas: Iterable[CNFFormula]):
        for cnf_formulas in formulas:
            if self.equivalent(cnf_formulas):
                return True
        return False
