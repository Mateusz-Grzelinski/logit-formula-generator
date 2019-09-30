from __future__ import annotations

from collections import Iterable

from src.ast.operands import LogicalOperand
from src.containers import ConstantLengthContainer
from src.containers.fol import LiteralContainer
from .folelement import FolElement
from .literal import Literal


class CNFClause(LiteralContainer, FolElement, container_implementation=ConstantLengthContainer):
    operand = LogicalOperand.AND

    def __init__(self, items: Iterable[Literal] = None, related_placeholder: CNFClausePlaceholder = None,
                 parent: CNFFormula = None, scope: CNFFormula = None, *args, **kwagrs):
        super().__init__(items=items, related_placeholder=related_placeholder, parent=parent, scope=scope, *args,
                         **kwagrs)

    def __str__(self):
        return 'cnf(' + '|'.join(str(l) for l in self.literals()) + ').'

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if isinstance(other, CNFClause):
            return super().__eq__(other)
        raise NotImplementedError

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

    def update_scope(self):
        from src.ast.fol import CNFFormula
        parent = self.parent
        while parent is not None:
            if isinstance(parent, CNFFormula):
                self.scope = parent
                break
            parent = parent.parent
