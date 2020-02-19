from typing import NoReturn

from logic_formula_generator.syntax_tree.first_order_logic.visitors.first_order_logic_visitor import FirstOrderLogicSyntaxTreeVisitor
from logic_formula_generator.syntax_tree.syntax_tree import FirstOrderLogicNode


class FOLFormulaInfoCollector(FirstOrderLogicSyntaxTreeVisitor):
    # todo
    def visit_pre(self, element: FirstOrderLogicNode) -> NoReturn:
        raise NotImplementedError
