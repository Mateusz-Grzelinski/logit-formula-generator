from __future__ import annotations

import json
import logging
import os
from enum import Enum
from inspect import isclass
from typing import NoReturn

from .tptp_header import TPTPHeader
from .._exporter import Exporter
from ...first_order_logic import CNFFormula


class SerializableJSONEncoder(json.JSONEncoder):
    """This encoder can encode Enum and classes that inherit Serializable
    Usage json.dumps(variable, cls=SerializableJSONEncoder)
    """

    def default(self, o):
        if isclass(o):
            return self._as_plain_dict(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

    def _as_plain_dict(self, o):
        """Convert to dict that holds only basic types"""
        # todo ignore variables that start with _
        class_dict = o.__dict__.copy()
        for key, value in o.__dict__.items():
            if key.startswith('_') or key.startswith(self.__class__.__name__):
                class_dict.pop(key)
                continue
            # recursion is not efficies, but is is easy
            if isclass(value):
                class_dict[key] = self._as_plain_dict(value)
        return class_dict


class TPTPExporter(Exporter):
    extension = '.p'

    def __init__(self, output_dir: str, statistics_to_file: bool = True, add_tptp_header=True):
        super().__init__(output_dir)
        self.add_tptp_header = add_tptp_header
        self.statistics_to_file = statistics_to_file

    def export(self, expression: CNFFormula, filename: str = '') -> NoReturn:
        if not isinstance(expression, CNFFormula):
            raise NotImplementedError('Other elements of syntax tree arte not properly supported')
        # by 'coincidence' default visualisation of first order logic is TPTP format :)
        formula_info = expression.get_info()
        filename = filename + self.extension

        if self.statistics_to_file:
            full_json_out_path = os.path.join(self.output_dir, filename + '.json')
            logging.info(f'Writing json to {full_json_out_path}')
            with open(full_json_out_path, 'w') as out_json:
                json.dump(formula_info.__dict__, out_json, indent=2, cls=SerializableJSONEncoder)

            full_out_path = os.path.join(self.output_dir, filename)
            with open(full_out_path, 'w') as out_file:
                logging.info(f'Writing formula to {full_out_path}')
                if self.add_tptp_header:
                    header = TPTPHeader()
                    header.read_from(formula_info)
                    header.output_file = filename
                    out_file.write(header.get_header())
                out_file.write(str(expression))
