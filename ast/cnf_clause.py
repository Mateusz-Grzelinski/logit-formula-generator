from __future__ import annotations

from typing import List

from ast.containers import LiteralContainer
from ast.literal import Literal
from ast.operands import LogicalOperand


class CNFClause(LiteralContainer):
    operand = LogicalOperand.AND

    def __init__(self, literals: List[Literal] = None):
        super().__init__(additional_containers=[], items=literals)

    def __str__(self):
        return 'cnf(' + ' | '.join(str(l) for l in self.literals()) + ').'



