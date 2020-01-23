from __future__ import annotations

from typing import Iterable

from ..syntax_tree import SyntaxTreeNode, FirstOrderLogicNode


class Functor(FirstOrderLogicNode):
    def __init__(self, name: str, children: Iterable[Term] = None):
        super().__init__(children=children)
        self.name = name

    def __hash__(self):
        return hash(self.name) ^ SyntaxTreeNode.__hash__(self)

    def __eq__(self, other):
        if isinstance(other, Functor):
            return hash(self.name) and SyntaxTreeNode.__eq__(self, other)
        elif isinstance(other, FirstOrderLogicNode):
            return False
        raise NotImplementedError

    def __str__(self):
        if len(list(self)) != 0:
            return f'{self.name}({",".join(str(t) for t in self)})'
        else:
            return f'{self.name}'

    @property
    def arity(self):
        return len(self)

    @property
    def is_recursive(self):
        return any(isinstance(t, Functor) for t in self)

    @property
    def recursion_depth(self):
        if self.is_recursive:
            return max(f.recursion_depth + 1 for f in self if isinstance(f, Functor))
        else:
            return 0

    @property
    def is_constant(self):
        return len(self) == 0
