from __future__ import annotations

from typing import List

from .ast_element import AstElement
from .containers import LiteralContainer
from .literal import Literal
from .operands import LogicalOperand


class CNFClause(LiteralContainer, AstElement):
    operand = LogicalOperand.AND

    def __init__(self, literals: List[Literal] = None, mutable=True):
        super().__init__(additional_containers=[], items=literals, mutable=mutable)

    def __str__(self):
        return 'cnf(' + ' | '.join(str(l) for l in self.literals()) + ').'

    @property
    def length(self):
        return len(self._items)

    @property
    def is_unit(self):
        return len(self._items) == 1
