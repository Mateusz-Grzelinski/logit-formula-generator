from __future__ import annotations

import io
from typing import NoReturn

from src.syntax_tree.propositional_temporal_logic import PTLFormula, Variable
from ..ptl_exporter import PropositionalTemporalLogicExporter


class InkresatExporter(PropositionalTemporalLogicExporter):
    extension = '.fml'

    def visit_variable(self, element: Variable):
        self.formula_buffer.write(''.join(connective.sign for connective in element.unary_connectives))
        self.formula_buffer.write(element.name)

    def visit_temporal_logic_formula_in_between_children(self, element: PTLFormula) -> NoReturn:
        self.formula_buffer.write(element.logical_connective.sign)

    def visit_temporal_logic_formula_pre(self, element: PTLFormula):
        if not self.context:
            self.formula_buffer.write('begin\n')
        elif len(element) != 1:
            self.formula_buffer.write('(')

    def visit_temporal_logic_formula_post(self, element: PTLFormula) -> NoReturn:
        if not self.context:
            self.formula_buffer.write('\nend')
        elif len(element) != 1:
            self.formula_buffer.write(')')

    def get_formula_as_string(self) -> io.StringIO:
        return self.formula_buffer
