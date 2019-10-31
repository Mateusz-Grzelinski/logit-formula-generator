from __future__ import annotations

from typing import Iterable, Set, Type

from ._cnf_clause import CNFClause
from ._cnf_formula_info import CNFFormulaInfo
from .._folelement import FOLElement
from ..._containers import Container


class CNFFormula(Container, FOLElement):
    def __init__(self, items: Iterable[CNFClause], *args,
                 **kwargs):
        super().__init__(items=items, *args, **kwargs)

    def __str__(self):
        return '\n'.join(str(c) for c in self.items(type=CNFClause))

    def __eq__(self, other):
        if isinstance(other, CNFFormula):
            return super().__eq__(other)
        raise NotImplementedError

    def get_info(self) -> CNFFormulaInfo:
        from src.ast.first_order_logic.conjunctive_normal_form.__cnf_formula_visitor import CNFFormulaVisitor
        walker = CNFFormulaVisitor()
        self._accept(walker)
        return walker.info

    @classmethod
    def contains(cls) -> Set[Type[FOLElement]]:
        from ._cnf_clause import CNFClause
        return {CNFClause}
