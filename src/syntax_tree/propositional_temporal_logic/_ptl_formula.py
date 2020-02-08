from __future__ import annotations

import io
import json
import os
import shutil
from typing import Set, Type, MutableSequence, NoReturn, Dict

from src.syntax_tree import ConnectiveProperties
from src.syntax_tree.propositional_temporal_logic.info.cnf_ptl_formula_info import \
    ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo
from ..syntax_tree import ChildrenType, TemporalLogicNode


class PTLFormula(TemporalLogicNode):
    """Propositional Temporal Logic"""

    def __init__(self, children: MutableSequence[ChildrenType], logical_connective: ConnectiveProperties):
        super().__init__(children)
        self.logical_connective = logical_connective

    @classmethod
    def contains(cls) -> Set[Type[TemporalLogicNode]]:
        from ._variable import Variable
        return {PTLFormula, Variable}

    def get_info(self) -> ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo:
        from src.syntax_tree.propositional_temporal_logic.visitors.cnf_ptl_formula_visitor import CNFPTLFormulaVisitor
        walker = CNFPTLFormulaVisitor()
        self._accept(walker)
        return walker.info

    def get_as_inkresat(self) -> io.StringIO:
        from .exporters.inkresat.inkresat_exporter import InkresatExporter
        exporter = InkresatExporter()
        self._accept(exporter)
        return exporter.get_formula_as_string()

    def save_to_file(self, path: str, formula_prefix: str = '') -> NoReturn:
        from src.syntax_tree.propositional_temporal_logic.exporters.inkresat.inkresat_exporter import InkresatExporter

        os.makedirs(os.path.dirname(path), exist_ok=True)
        path += InkresatExporter.extension

        buff = self.get_as_inkresat()
        with open(path, 'w') as out_file:
            if formula_prefix:
                out_file.write(formula_prefix)
            buff.seek(0)
            shutil.copyfileobj(buff, out_file)

    def save_info_to_file(self, path: str, additional_statistics: Dict = None) -> NoReturn:
        """Save statistics to json file"""
        info = self.get_info()
        info.additional_statistics = additional_statistics
        path += '.json'

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as out_file:
            json.dump(info.__dict__, fp=out_file)
