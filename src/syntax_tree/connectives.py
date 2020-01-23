from dataclasses import dataclass, field
from typing import Optional, Literal

# LogicalConnective = Union[ConnectiveEnum, str]

LOGICS = Literal['FirstOrderLogic', 'TemporalLogic']


@dataclass(frozen=True, eq=True)
class ConnectiveProperties:
    arity: int = field(compare=False, hash=False)
    commutative: Optional[bool] = field(compare=False, hash=False, default=None)
    sign: str = ''

    def __str__(self):
        return self.sign


class Connective:
    pass


class LogicalConnective(Connective):
    AND = ConnectiveProperties(sign='&', arity=2, commutative=True)
    OR = ConnectiveProperties(sign='|', arity=2, commutative=True)
    NOT = ConnectiveProperties(sign='~', arity=1)
    IMPLY = ConnectiveProperties(sign='=>', arity=2, commutative=False)
    BICONDITION = ConnectiveProperties(sign='<=>', arity=2, commutative=True)


class MathConnective(Connective):
    EQUAL = ConnectiveProperties(sign='==', arity=2, commutative=True)
    NOT_EQUAL = ConnectiveProperties(sign='!=', arity=2, commutative=True)


class TemporalLogicConnective(LogicalConnective):
    ALWAYS = ConnectiveProperties(sign='[]', arity=1)
    """Always, also known as box"""
    EVENTUALLY = ConnectiveProperties(sign='<>', arity=1)
    """Eventually, also known as diamond"""


_connectives_lookup_table = {
    '': None,
    'and': LogicalConnective.AND,
    '&': LogicalConnective.AND,
    'or': LogicalConnective.OR,
    '|': LogicalConnective.OR,
    '-': LogicalConnective.NOT,
    '~': LogicalConnective.NOT,
    'not': LogicalConnective.NOT,
    '=': MathConnective.EQUAL,
    '==': MathConnective.EQUAL,
    '!=': MathConnective.NOT_EQUAL,
    '[]': TemporalLogicConnective.EVENTUALLY,
    '<>': TemporalLogicConnective.EVENTUALLY,
}


def get_connective_properties(operand: str) -> ConnectiveProperties:
    return _connectives_lookup_table[operand]
