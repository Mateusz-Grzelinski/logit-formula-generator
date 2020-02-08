import io

from src.syntax_tree.exporters import Exporter
from src.syntax_tree.propositional_temporal_logic.visitors.propositional_temporal_logic_visitor import \
    PropositionalTemporalLogicVisitor


class PropositionalTemporalLogicExporter(PropositionalTemporalLogicVisitor, Exporter):
    def __init__(self):
        super().__init__()
        self.formula_buffer = io.StringIO()

    def get_formula_as_string(self) -> io.StringIO:
        raise NotImplementedError
