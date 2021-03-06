"""This temporal logic syntax tree is based on InKreSAT input format (relational variables are not implemented)"""
from ._ptl_formula import PTLFormula
from ._variable import Variable

__all__ = [
    'PTLFormula',
    'Variable'
]
