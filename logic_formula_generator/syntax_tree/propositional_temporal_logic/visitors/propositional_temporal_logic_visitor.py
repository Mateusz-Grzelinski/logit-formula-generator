from __future__ import annotations

from typing import NoReturn

from .._ptl_formula import PTLFormula
from .._variable import Variable
from ...syntax_tree_visitor import SyntaxTreeVisitor


class PropositionalTemporalLogicVisitor(SyntaxTreeVisitor):

    def __init__(self) -> None:
        self.context = []
        super().__init__()

    def visit_pre(self, element: TemporalLogicNode) -> NoReturn:
        if isinstance(element, Variable):
            self.visit_variable(element)
        elif isinstance(element, PTLFormula):
            self.visit_temporal_logic_formula_pre(element)
        else:
            assert False, f'Unknown element for visitor {type(element)}, {element}'
        self.context.append(element)

    def visit_in_between_children(self, element: TemporalLogicNode) -> NoReturn:
        if isinstance(element, PTLFormula):
            self.visit_temporal_logic_formula_in_between_children(element)

    def visit_post(self, element: TemporalLogicNode) -> NoReturn:
        self.context.pop()
        if isinstance(element, PTLFormula):
            self.visit_temporal_logic_formula_post(element)

    def visit_variable(self, element: Variable):
        pass

    def visit_temporal_logic_formula_in_between_children(self, element: PTLFormula) -> NoReturn:
        pass

    def visit_temporal_logic_formula_pre(self, element: PTLFormula):
        pass

    def visit_temporal_logic_formula_post(self, element: PTLFormula) -> NoReturn:
        pass
