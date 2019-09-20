from __future__ import annotations

from typing import List

from .ast_element import AstElement
from .containers import LiteralContainer
from .literal import Literal
from .operands import LogicalOperand


class CNFClause(LiteralContainer, AstElement):
    operand = LogicalOperand.AND

    def __init__(self, literals: List[Literal] = None, mutable=True, related_placeholder: CNFClausePlaceholder = None):
        LiteralContainer.__init__(self, additional_containers=[], items=literals, mutable=mutable)
        AstElement.__init__(self, related_placeholder=related_placeholder)

    def __str__(self):
        return 'cnf(' + ' | '.join(str(l) for l in self.literals()) + ').'

    def __hash__(self):
        return hash(i for i in self._items)

    def __eq__(self, other):
        if isinstance(other, CNFClause):
            return len(self._items) == len(other._items) and all(i == j for i, j in zip(self._items, other._items))
        return False

    @property
    def length(self):
        return len(self._items)

    @property
    def is_unit(self):
        return len(self._items) == 1

    @property
    def number_of_singleton_variables(self) -> int:
        variables = list(self.variables())
        singleton_vars = set([x for x in variables if variables.count(x) == 1])
        return len(singleton_vars)
