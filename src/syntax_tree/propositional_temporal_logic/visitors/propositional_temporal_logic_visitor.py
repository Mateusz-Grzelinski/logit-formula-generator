from __future__ import annotations

from .._ptl_formula import PTLFormula
from .._variable import Variable
from ...syntax_tree_visitor import SyntaxTreeVisitor


class PropositionalTemporalLogicVisitor(SyntaxTreeVisitor):

    def visit(self, element: TemporalLogicElement):
        if isinstance(element, Variable):
            self.visit_variable(element)
        elif isinstance(element, PTLFormula):
            self.visit_temporal_logic_formula(element)
        else:
            assert False, f'Unknown element for visitor {type(element)}, {element}'

    def visit_variable(self, element: Variable):
        pass

    def visit_temporal_logic_formula(self, element: PTLFormula):
        pass
