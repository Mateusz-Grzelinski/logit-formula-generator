from __future__ import annotations

from typing import Iterable, Literal

from ._variable import Variable
from ..syntax_tree import FirstOrderLogicNode


class Quantifier(FirstOrderLogicNode):
    def __init__(self, children: Iterable[FirstOrderLogicFormula], unary_connective: Iterable,
                 type: Literal['universal', 'existential']):
        self.unary_connective = tuple(unary_connective)
        self.type = type
        super().__init__(children)

    def __hash__(self):
        return hash(self.type) ^ hash(self.unary_connective) ^ FirstOrderLogicNode.__hash__(self)

    def __eq__(self, other):
        if isinstance(other, Quantifier):
            return self.type == other.type and FirstOrderLogicNode.__eq__(self, other)
        elif isinstance(other, FirstOrderLogicNode):
            return False
        raise NotImplementedError

    @property
    def is_universal(self):
        return self.type == 'universal'

    @property
    def is_existential(self):
        return self.type == 'existential'

    def __str__(self):
        variables = ', '.join(set(str(i) for i in self.recursive_nodes(type=Variable)))
        formula = f'[{variables}]:{str(self)}'
        if self.is_existential:
            return '?' + formula
        else:
            return '!' + formula
