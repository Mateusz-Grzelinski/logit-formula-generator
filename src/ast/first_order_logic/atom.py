from __future__ import annotations

from typing import Optional, Union, Iterable, Set, Type

from src.ast import connectives
from src.ast.connectives import MathConnective
from src.ast.containers import Container
from .folelement import FOLElement
from .term import Term


class Atom(Container, FOLElement):
    def __init__(self, items: Iterable[Term, Predicate], connective: Optional[Union[str, MathConnective]],
                 *args, **kwargs):
        super().__init__(items=items, *args, **kwargs)

        if connective is None:
            self.connective_properties = None
        elif isinstance(connective, str) or isinstance(connective, MathConnective):
            self.connective_properties = connectives.get_connective_properties(connective)
        else:
            raise TypeError(f'invalid argument type for field connective: {connective}')

    def __hash__(self):
        return hash(self.connective_properties) ^ Container.__hash__(self)

    def __eq__(self, other):
        if isinstance(other, Atom):
            return self.connective_properties == other.connective_properties and Container.__eq__(self, other)
        raise NotImplementedError

    def __str__(self):
        # handle incorrect arity vs len(self._items)
        if self.connective_properties is None or self.connective_properties.arity == 1:
            return str(self._items[0]) if self._items else ''

        # default visualization
        if self.connective_properties.connective == MathConnective.EQUAL:
            return '(' + ' = '.join(str(i) for i in self._items) + ')'
        if self.connective_properties.connective == MathConnective.NOT_EQUAL:
            return '(' + ' != '.join(str(i) for i in self._items) + ')'

        raise Exception(f'{self.connective_properties} does not have default visualization')

    @classmethod
    def contains(cls) -> Set[Type[FOLElement]]:
        from src.ast.first_order_logic import Variable
        from .predicate import Predicate
        return {Predicate, Variable}

    @property
    def arity(self):
        return len(self._items)

