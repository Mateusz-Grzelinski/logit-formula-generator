from __future__ import annotations

import io
import json
import os
import shutil
import typing
from typing import Iterable

from src.data_model._fol_formula_info import FirstOrderLogicFormulaInfo
from src.syntax_tree import ConnectiveProperties
from ._atom import Atom
from ._quantifier import Quantifier
from ..syntax_tree import FirstOrderLogicNode


class FirstOrderLogicFormula(FirstOrderLogicNode):
    def __init__(self, children: Iterable[Atom, Quantifier, FirstOrderLogicFormula],
                 binary_logical_connective: ConnectiveProperties = None,
                 unary_connective: Iterable[ConnectiveProperties] = None):
        super().__init__(children)
        self.unary_connective = list(unary_connective) if unary_connective else []
        self.logical_connective = binary_logical_connective

    def __str__(self):
        unary_connectives = ' '.join(str(i) for i in self.unary_connective)
        return unary_connectives + self.logical_connective.sign.join(str(i) for i in self)

    def get_as_tptp(self) -> io.StringIO:
        from .exporters.tptp import TPTPExporter
        exporter = TPTPExporter()
        self._accept(exporter)
        return exporter.get_formula_as_string()

    def get_tptp_header(self, info: FirstOrderLogicFormulaInfo) -> str:
        # todo implement
        raise NotImplementedError

    def get_formula_info(self) -> FirstOrderLogicFormulaInfo:
        # todo implement
        raise NotImplementedError

    def save_to_file(self, path: str, formula_prefix: str = '',
                     format: typing.Literal['tptp'] = 'tptp') -> typing.NoReturn:
        from src.syntax_tree.first_order_logic.exporters.tptp import TPTPExporter
        assert format == 'tptp', 'Only TPTP format is supported'

        os.makedirs(os.path.dirname(path), exist_ok=True)
        path += TPTPExporter.extension

        buff = self.get_as_tptp()
        with open(path, 'w') as out_file:
            if formula_prefix:
                out_file.write(formula_prefix)
            buff.seek(0)
            shutil.copyfileobj(buff, out_file)

    def save_info_to_file(self, path: str, additional_statistics: typing.Dict = None) -> typing.NoReturn:
        """Save statistics to json file"""
        info = self.get_formula_info()
        info.additional_statistics = additional_statistics
        path += '.json'

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as out_file:
            json.dump(info.__dict__, fp=out_file)
