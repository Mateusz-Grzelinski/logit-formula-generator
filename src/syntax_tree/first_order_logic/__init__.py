from typing import Union

from ._atom import Atom
from ._fol_formula import FirstOrderLogicFormula
from ._functor import Functor
from ._predicate import Predicate
from ._quantifier import Quantifier
from ._variable import Variable
from .conjunctive_normal_form import CNFClause
from .conjunctive_normal_form import CNFFOLFormulaInfo
from .conjunctive_normal_form import CNFFirstOrderLogicFormula

Term = Union[Variable, Functor]

__all__ = [
    'Term',
    'Variable',
    'Functor',
    'Predicate',
    'Atom',
    'FirstOrderLogicFormula',
    'Quantifier',
    'CNFClause',
    'CNFFirstOrderLogicFormula',
    'CNFFOLFormulaInfo',
]
