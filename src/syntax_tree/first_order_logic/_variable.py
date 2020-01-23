from __future__ import annotations

from ..syntax_tree import FirstOrderLogicNode


class Variable(FirstOrderLogicNode):
    def __init__(self, name: str):
        super().__init__(children=[])
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        elif isinstance(other, FirstOrderLogicNode):
            return False
        raise NotImplementedError

    def __str__(self):
        return self.name
