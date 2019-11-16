from __future__ import annotations

from typing import Iterable, Literal, Union

from ._first_order_logic_element import FirstOrderLogicElement
from ._variable import Variable
from .._ast_element import AstElement
from .._containers import Container

MODE = Literal['all', 'exist']


class Quantifier(Container, AstElement):
    UNIVERSAL = 'all'
    EXISTENTIAL = 'exist'

    def __init__(self, items: Iterable[Formula], type: Union['all', 'exists'], *args, **kwargs):
        self.type = type
        super().__init__(items, *args, **kwargs)

    def __hash__(self):
        return hash(self.type) ^ Container.__hash__(self)

    def __eq__(self, other):
        if isinstance(other, Quantifier):
            return self.type == other.type and Container.__eq__(self, other)
        elif isinstance(other, FirstOrderLogicElement):
            return False
        raise NotImplementedError


class UniversalQuantifier(Quantifier):
    def __init__(self, items: Iterable[Formula], *args, **kwargs):
        super().__init__(items=items, type=Quantifier.UNIVERSAL, *args, **kwargs)

    def __str__(self):
        variables = ', '.join(set(str(i) for i in self.items(type=Variable)))
        return f'![{variables}]:{str(self)}'


class ExistentialQuantifier(Quantifier):
    def __init__(self, items: Iterable[Formula], *args, **kwargs):
        super().__init__(items=items, type=Quantifier.EXISTENTIAL, *args, **kwargs)

    def __str__(self):
        variables = ', '.join(set(str(i) for i in self.items(type=Variable)))
        return f'?[{variables}]:{str(self)}'
