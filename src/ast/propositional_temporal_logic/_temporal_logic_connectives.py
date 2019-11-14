from enum import Enum

from src.ast._connectives import ConnectiveEnum


class TemporalLogicConnective(ConnectiveEnum, Enum):
    ALWAYS = '[]'
    """Always, also known as box"""
    EVENTUALLY = '<>'
    """Eventually, also known as diamond"""
