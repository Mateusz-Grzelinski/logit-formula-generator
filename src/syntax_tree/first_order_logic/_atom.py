from __future__ import annotations

from typing import Iterable

from ..connectives import ConnectiveProperties, LogicalConnective, MathConnective
from ..syntax_tree import SyntaxTreeNode, FirstOrderLogicNode


class Atom(FirstOrderLogicNode):
    def __init__(self, children: Iterable[Term, Predicate], unary_connective: Iterable[LogicalConnective],
                 math_connective: ConnectiveProperties = None):
        super().__init__(children=children)
        self.unary_connectives = list(unary_connective)
        self.math_connective = math_connective

    def __hash__(self):
        return hash(self.math_connective.sign) ^ SyntaxTreeNode.__hash__(self)

    def __eq__(self, other):
        # todo compare unary connectives
        if isinstance(other, Atom):
            return self.math_connective.sign == other.math_connective.sign and \
                   SyntaxTreeNode.__eq__(self, other)
        elif isinstance(other, FirstOrderLogicNode):
            return False
        raise NotImplementedError

    def __str__(self):
        # handle incorrect arity vs len(self._items)
        if self.math_connective is None:
            return str(self[0]) if len(self) else ''

        # default visualization
        return '(' + self.math_connective.sign.join(str(i) for i in self) + ')'

    @property
    def arity(self):
        return len(self)

    @property
    def is_equality(self):
        return MathConnective.EQUAL == self.math_connective or MathConnective.NOT_EQUAL == self.math_connective
