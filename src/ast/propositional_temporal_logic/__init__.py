"""This temporal logic syntax tree is based on InKreSAT input format (relational variables are not implemented)"""
from ._formula import Formula
from ._temporal_logic_connectives import TemporalLogicConnective
from ._variable import Variable

__all__ = [
    'Formula',
    'Variable',
    'TemporalLogicConnective'
]
