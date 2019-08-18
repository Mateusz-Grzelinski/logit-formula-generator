from __future__ import annotations
from typing import List, Any

from docutils.nodes import literal

from ast.literal import Literal
from ast.operands import LogicalOperand
from containers.atom_container import AtomContainer
from containers.container import Container
from containers.literal_container import LiteralContainer


class CNFClause(LiteralContainer):
    operand = LogicalOperand.AND

    def __init__(self, literals: List[Literal] = None):
        super().__init__(additional_containers=[], items=literals)

    def __str__(self):
        return 'cnf(' + ' | '.join(str(l) for l in self.literals()) + ').'



