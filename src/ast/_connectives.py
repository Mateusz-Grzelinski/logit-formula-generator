from dataclasses import dataclass, field
from enum import Enum
from typing import Union, Optional


@dataclass(frozen=True, eq=True)
class ConnectiveProperties:
    connective: Optional[Enum]
    arity: int = field(compare=False, hash=False)
    commutative: bool = field(compare=False, hash=False)


class ConnectiveEnum:
    pass


class LogicalConnective(ConnectiveEnum, Enum):
    """Operand and arity"""
    AND = '∧'
    OR = 'v'
    NOT = '~'
    IMPLY = '=>'
    BICONDITION = '<=>'


class MathConnective(ConnectiveEnum, Enum):
    """Operand and arity"""
    EQUAL = '='
    NOT_EQUAL = '!='


_connectives_lookup_table = None


def _init_lookup_table():
    # to avoid circular deps
    from src.ast.propositional_temporal_logic._temporal_logic_connectives import TemporalLogicConnective
    _no_connective = ConnectiveProperties(connective=None, arity=1, commutative=False)
    _and = ConnectiveProperties(connective=LogicalConnective.AND, arity=2, commutative=True)
    _or = ConnectiveProperties(connective=LogicalConnective.OR, arity=2, commutative=True)
    _not = ConnectiveProperties(connective=LogicalConnective.NOT, arity=2, commutative=False)
    _equal = ConnectiveProperties(connective=MathConnective.EQUAL, arity=2, commutative=True)
    _not_equal = ConnectiveProperties(connective=MathConnective.NOT_EQUAL, arity=2, commutative=True)

    _always = ConnectiveProperties(connective=TemporalLogicConnective.ALWAYS, arity=1, commutative=False)
    _eventually = ConnectiveProperties(connective=TemporalLogicConnective.EVENTUALLY, arity=1, commutative=False)

    global _connectives_lookup_table
    _connectives_lookup_table = {
        '': _no_connective,
        None: _no_connective,
        LogicalConnective.AND: _and,
        'and': _and,
        '&': _and,
        LogicalConnective.OR: _or,
        'or': _or,
        '|': _or,
        LogicalConnective.NOT: _not,
        '-': _not,
        '~': _not,
        'not': _not,
        MathConnective.EQUAL: _equal,
        '=': _equal,
        '==': _equal,
        MathConnective.NOT_EQUAL: _not_equal,
        '!=': _not_equal,
        TemporalLogicConnective.ALWAYS: _always,
        '[]': _always,
        TemporalLogicConnective.EVENTUALLY: _eventually,
        '<>': _eventually,
    }


def get_connective_properties(operand: Union[str, MathConnective, LogicalConnective]) -> ConnectiveProperties:
    return _connectives_lookup_table[operand]


_init_lookup_table()
