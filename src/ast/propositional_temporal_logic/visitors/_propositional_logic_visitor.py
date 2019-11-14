from __future__ import annotations

from .._formula import Formula
from .._variable import Variable
from ..._ast_visitor import AstVisitor


class FOLAstVisitor(AstVisitor):

    def visit(self, element: TemporalLogicElement):
        if isinstance(element, Variable):
            self.visit_variable(element)
        elif isinstance(element, Formula):
            self.visit_temporal_logic_formula(element)
        else:
            assert False, f'Unknown element for visitor {type(element)}, {element}'

    def visit_variable(self, element: Variable):
        pass

    def visit_temporal_logic_formula(self, element: Formula):
        pass
