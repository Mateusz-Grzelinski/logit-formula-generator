from __future__ import annotations

from typing import Iterable

from ..syntax_tree import SyntaxTreeNode, FirstOrderLogicNode


class Predicate(FirstOrderLogicNode):
    def __init__(self, name: str, children: Iterable[Variable, Functor] = None):
        self.name = name
        super().__init__(children=children)

    def __str__(self):
        if len(self) != 0:
            return f'{self.name}({",".join(str(term) for term in self)})'
        else:
            return f'{self.name}'

    def __hash__(self):
        return hash(self.name) ^ SyntaxTreeNode.__hash__(self)

    def __eq__(self, other):
        if isinstance(other, Predicate):
            return self.name == other.name and SyntaxTreeNode.__eq__(self, other)
        elif isinstance(other, FirstOrderLogicNode):
            return False
        raise NotImplementedError

    @property
    def arity(self):
        return len(self)
