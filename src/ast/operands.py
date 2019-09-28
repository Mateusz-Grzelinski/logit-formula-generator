from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Union

from src.ast.ast_element import AstElement


class LogicalOperand(Enum):
    """Operand and arity"""
    AND = 2
    OR = 2
    NOT = 1


class MathOperand(Enum):
    """Operand and arity"""
    EQUAL = 2
    NOT_EQUAL = 2


@dataclass
class Connective(AstElement):
    operand: Union[MathOperand, LogicalOperand]
    allowed_symbols: ClassVar[str] = set()

    def __hash__(self) -> int:
        return hash(self.operand.name)


if __name__ == '__main__':
    print(LogicalOperand.NOT)
    print(MathOperand.NOT_EQUAL)
