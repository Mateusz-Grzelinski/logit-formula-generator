"""first_order_logic - First Order Logic"""
from ._atom import Atom
from ._functor import Functor
from ._predicate import Predicate
from ._term import Term
from ._variable import Variable
from .conjunctive_normal_form import CNFClause
from .conjunctive_normal_form import CNFFormula
from .conjunctive_normal_form import Literal

__all__ = [
    'Term',
    'Variable',
    'Functor',
    'Predicate',
    'Atom',
    'Literal',
    'CNFClause',
    'CNFFormula',
]
