from __future__ import annotations

import json
import os
import textwrap
from typing import NoReturn, Callable

from .._exporter import Exporter


class InkresatExporter(Exporter):
    extension = '.fml'
    comment_sign = '#'

    def __init__(self, filename_handle: Callable[[PTLFormulaInfo], str], output_dir: str, statistics_to_file=True):
        super().__init__(filename_handle, output_dir)
        self.statistics_to_file = statistics_to_file

    def export(self, expression: PTLFormula, filename_suffix: str = '') -> NoReturn:
        from src.ast.propositional_temporal_logic import PTLFormula
        if not isinstance(expression, PTLFormula):
            raise NotImplementedError('Other elements of syntax tree arte not properly supported')
        # by 'coincidence' default visualisation of first order logic is TPTP format :)
        from src.ast.propositional_temporal_logic.info.cnf_ptl_formula_info import CNFPTLFormulaInfo
        formula_info: CNFPTLFormulaInfo = expression.get_info()
        filename = self.filename_handle(formula_info) + filename_suffix

        if self.statistics_to_file:
            full_json_out_path = os.path.join(self.output_dir, filename + '.json')
            with open(full_json_out_path, 'w') as out_json:
                json.dump(formula_info.__dict__, out_json, indent=2)

        full_out_path = os.path.join(self.output_dir, filename + self.extension)
        with open(full_out_path, 'w') as out_file:
            print(f'Writing formula to {full_out_path}')
            if not self.statistics_to_file:
                text = json.dumps(**formula_info.__dict__, indent=2)
                text = textwrap.indent(text=text, prefix=f'{self.comment_sign} ', predicate=lambda line: True) + '\n'
                out_file.write(text)
            out_file.write(str(expression))
