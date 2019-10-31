from enum import Enum

from .._connectives import ConnectiveEnum


class TemporalLogicConnective(ConnectiveEnum, Enum):
    ALWAYS = '[]'
    """Also known as box"""
    EVENTUALLY = '<>'
    """Also known as diamond"""
