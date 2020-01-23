from __future__ import annotations

import json
import logging
import os
import textwrap
from typing import NoReturn, Dict

from .._exporter import Exporter


class InkresatExporter(Exporter):
    extension = '.fml'
    comment_sign = '#'

    def __init__(self, output_dir: str, statistics_to_file=True, additional_statistics: Dict = None):
        super().__init__(output_dir, additional_statistics)
        self.statistics_to_file = statistics_to_file

    def export(self, expression: PTLFormula, filename: str = '') -> NoReturn:
        # by 'coincidence' default visualisation of teporal logic is inkresat
        from src.syntax_tree.propositional_temporal_logic import PTLFormula
        from src.syntax_tree.propositional_temporal_logic.info.cnf_ptl_formula_info import \
            ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo

        if not isinstance(expression, PTLFormula):
            raise NotImplementedError('Other elements of syntax tree arte not properly supported')
        formula_info: ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo = expression.get_info()
        formula_info.additional_statistics = self.additional_statistics
        filename = filename + self.extension

        if self.statistics_to_file:
            full_json_out_path = os.path.join(self.output_dir, filename + '.json')
            logging.debug(f'Writing json to {full_json_out_path}')
            with open(full_json_out_path, 'w') as out_json:
                json.dump(formula_info.__dict__, out_json, indent=2)

        full_out_path = os.path.join(self.output_dir, filename)
        with open(full_out_path, 'w') as out_file:
            logging.debug(f'Writing formula to {full_out_path}')
            if not self.statistics_to_file:
                text = json.dumps(**formula_info.__dict__, indent=2)
                text = textwrap.indent(text=text, prefix=f'{self.comment_sign} ', predicate=lambda line: True) + '\n'
                out_file.write(text)
            out_file.write(str(expression))
