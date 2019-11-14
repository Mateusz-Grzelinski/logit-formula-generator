from __future__ import annotations

from ._first_order_logic_element import FirstOrderLogicElement
from ._term import Term


class Variable(Term, FirstOrderLogicElement):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        elif isinstance(other, FirstOrderLogicElement):
            return False
        raise NotImplementedError
