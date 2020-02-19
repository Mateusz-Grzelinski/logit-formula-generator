import io

from logic_formula_generator.syntax_tree.exporters import Exporter
from logic_formula_generator.syntax_tree.first_order_logic.visitors.first_order_logic_visitor import FirstOrderLogicSyntaxTreeVisitor


class FirstOrderLogicExporter(FirstOrderLogicSyntaxTreeVisitor, Exporter):
    def __init__(self):
        super().__init__()
        self.formula_buffer = io.StringIO()

    def get_formula_as_string(self) -> io.StringIO:
        return self.formula_buffer
