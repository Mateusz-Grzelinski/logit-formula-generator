from __future__ import annotations

import os
from typing import NoReturn, Callable

from .tptp_header import TPTPHeader
from .._exporter import Exporter
from ...first_order_logic import CNFFormula, CNFFormulaInfo


class TPTPExporter(Exporter):
    extension = '.p'

    def __init__(self, filename_handle: Callable[[CNFFormulaInfo], str], output_dir: str):
        super().__init__(filename_handle, output_dir)

    def export(self, expression: CNFFormula, filename_suffix: str = '') -> NoReturn:
        if not isinstance(expression, CNFFormula):
            raise NotImplementedError('Other elements of syntax tree arte not properly supported')
        # by 'coincidence' default visualisation of first order logic is TPTP format :)
        formula_info = expression.get_info()
        filename = self.filename_handle(formula_info) + filename_suffix + self.extension

        header = TPTPHeader()
        header.read_from(formula_info)
        header.output_file = filename

        full_out_path = os.path.join(self.output_dir, filename)
        with open(full_out_path, 'w') as out_file:
            print(f'Writing formula to {full_out_path}')
            out_file.write(header.get_header() + str(expression))
