from dataclasses import dataclass, field
from enum import Enum
from typing import Union, Optional


@dataclass(frozen=True, eq=True)
class ConnectiveProperties:
    connective: Optional[Enum]
    arity: int = field(compare=False, hash=False)
    commutative: bool = field(compare=False, hash=False)


class LogicalConnective(Enum):
    """Operand and arity"""
    AND = '∧'
    OR = 'v'
    NOT = '~'
    IMPLY = '=>'
    BICONDITION = '<=>'


class MathConnective(Enum):
    """Operand and arity"""
    EQUAL = '='
    NOT_EQUAL = '!='


_no_connective = ConnectiveProperties(connective=None, arity=1, commutative=False)
_and = ConnectiveProperties(connective=LogicalConnective.AND, arity=2, commutative=True)
_or = ConnectiveProperties(connective=LogicalConnective.OR, arity=2, commutative=True)
_not = ConnectiveProperties(connective=LogicalConnective.NOT, arity=2, commutative=False)
_equal = ConnectiveProperties(connective=MathConnective.EQUAL, arity=2, commutative=True)
_not_equal = ConnectiveProperties(connective=MathConnective.NOT_EQUAL, arity=2, commutative=True)

operand_lookup_table = {
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
    '!=': _not_equal
}


def get_operand_properties(operand: Union[str, MathConnective, LogicalConnective]) -> ConnectiveProperties:
    return operand_lookup_table[operand]
