from __future__ import annotations

from typing import Union

from src.ast.first_order_logic import Atom, CNFClause, Functor, Predicate, Variable, CNFFormula


class TPTPExporter:
    @staticmethod
    def cnf_export(expression: Union[Functor, Variable, Predicate, Atom, Literal, CNFClause, CNFFormula]) -> str:
        raise NotImplemented
