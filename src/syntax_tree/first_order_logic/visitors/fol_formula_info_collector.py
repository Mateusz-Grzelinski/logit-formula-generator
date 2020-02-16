from typing import NoReturn

from src.syntax_tree.first_order_logic.visitors.first_order_logic_visitor import FirstOrderLogicSyntaxTreeVisitor
from src.syntax_tree.syntax_tree import FirstOrderLogicNode


class FOLFormulaInfoCollector(FirstOrderLogicSyntaxTreeVisitor):
    # todo
    def visit_pre(self, element: FirstOrderLogicNode) -> NoReturn:
        raise NotImplementedError
