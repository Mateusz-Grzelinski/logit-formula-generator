from typing import Iterable

from logic_formula_generator.syntax_tree import ConnectiveProperties
from ..syntax_tree import TemporalLogicNode


class Variable(TemporalLogicNode):
    def __init__(self, name: str, unary_connectives: Iterable[ConnectiveProperties]):
        super().__init__(children=[])
        self.unary_connectives = list(unary_connectives)
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        raise NotImplementedError

    def __str__(self):
        return ''.join(i.sign for i in self.unary_connectives) + self.name
