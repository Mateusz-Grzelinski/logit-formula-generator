from dataclasses import dataclass, field
from enum import Enum
from typing import Union, Optional


@dataclass(frozen=True, eq=True)
class OperandProperties:
    operand: Optional[Enum]
    arity: int = field(compare=False, hash=False)
    commutative: bool = field(compare=False, hash=False)


class LogicalOperand(Enum):
    """Operand and arity"""
    AND = 'and'
    OR = 'or'
    NOT = '~'


class MathOperand(Enum):
    """Operand and arity"""
    EQUAL = '='
    NOT_EQUAL = '!='


_no_operand = OperandProperties(operand=None, arity=1, commutative=False)
_and = OperandProperties(operand=LogicalOperand.AND, arity=2, commutative=True)
_or = OperandProperties(operand=LogicalOperand.OR, arity=2, commutative=True)
_not = OperandProperties(operand=LogicalOperand.NOT, arity=2, commutative=False)
_equal = OperandProperties(operand=MathOperand.EQUAL, arity=2, commutative=True)
_not_equal = OperandProperties(operand=MathOperand.NOT_EQUAL, arity=2, commutative=True)

operand_lookup_table = {
    '': _no_operand,
    None: _no_operand,
    LogicalOperand.AND: _and,
    'and': _and,
    '&': _and,
    LogicalOperand.OR: _or,
    'or': _or,
    '|': _or,
    LogicalOperand.NOT: _not,
    '-': _not,
    '~': _not,
    'not': _not,
    MathOperand.EQUAL: _equal,
    '=': _equal,
    '==': _equal,
    MathOperand.NOT_EQUAL: _not_equal,
    '!=': _not_equal
}


def get_operand_properties(operand: Union[str, MathOperand, LogicalOperand]) -> OperandProperties:
    return operand_lookup_table[operand]
