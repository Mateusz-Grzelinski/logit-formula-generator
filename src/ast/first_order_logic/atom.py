from __future__ import annotations

from typing import Optional, Union, Iterable, Set, Type

from src.ast import operands
from src.ast.operands import MathOperand
from src.containers.fol import PredicateContainer
from src.containers.fol import TermContainer
from .folelement import FolElement
from .predicate import Predicate
from .term import Term


class Atom(TermContainer, PredicateContainer, FolElement):
    def __init__(self, items: Iterable[Term, Predicate], connective: Optional[Union[str, MathOperand]],
                 related_placeholder: AtomPlaceholder = None, parent: CNFFormula = None, scope: CNFFormula = None,
                 *args, **kwargs):
        super().__init__(items=items, related_placeholder=related_placeholder, parent=parent,
                         scope=scope, *args, **kwargs)

        if connective is None:
            self.connective_properties = None
        elif isinstance(connective, str) or isinstance(connective, MathOperand):
            self.connective_properties = operands.get_operand_properties(connective)
        else:
            raise TypeError(f'invalid argument type for field connective: {connective}')

    def __hash__(self):
        return hash(self.connective_properties) ^ PredicateContainer.__hash__(self)

    def __eq__(self, other):
        if isinstance(other, Atom):
            return self.connective_properties == other.connective_properties and PredicateContainer.__eq__(self, other)
        raise NotImplementedError

    def __str__(self):
        # handle incorrect arity vs len(self._items)
        if self.connective_properties is None or self.connective_properties.arity == 1:
            return str(self._items[0]) if self._items else ''

        # default visualization
        if self.connective_properties.operand == MathOperand.EQUAL:
            return '(' + ' = '.join(str(i) for i in self._items) + ')'
        if self.connective_properties.operand == MathOperand.NOT_EQUAL:
            return '(' + ' != '.join(str(i) for i in self._items) + ')'

        raise Exception(f'{self.connective_properties} does not have default visualization')

    @classmethod
    def contains(cls) -> Set[Type]:
        return PredicateContainer.contains().union()

    @property
    def arity(self):
        return len(self._items)

    def update_scope(self):
        from src.ast.first_order_logic import CNFFormula
        parent = self.parent
        while parent is not None:
            if isinstance(parent, CNFFormula):
                self.scope = parent
                break
            parent = parent.parent
