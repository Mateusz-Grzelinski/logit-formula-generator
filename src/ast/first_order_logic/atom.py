from __future__ import annotations

from typing import Optional, Union, Dict, Iterable, Set, Type

from src.ast.operands import MathOperand
from src.containers import ImmutableContainer
from src.containers.fol import PredicateContainer
from src.containers.fol import TermContainer
from .folelement import FolElement
from .predicate import Predicate
from .term import Term


class Atom(TermContainer, PredicateContainer, FolElement, container_implementation=ImmutableContainer):
    """Atom is every propositional statement (statement that can be assigned true or false):
    atom is logical statement - it evaluates to true of false
    Examples:
    - p(X)
    - p(f(X))
    - f(X) = f(Y)  # f is functor
    - p(X) = p(Y)
    - X != Y  # X, Y are variable
    - X  # is single var allowed?
    - f(a)  # is single functor allowed?

    Atom is not:
    - standalone functor
    - quantifier
    - expresion composed of logical connective (not, and, or, implies...)

     """
    allowed_connective: Dict[str, MathOperand] = {
        '': None,  # special case - no connective
        '=': MathOperand.EQUAL,
        '!=': MathOperand.NOT_EQUAL
    }
    """key: operation symbol, value: arity"""

    def __init__(self, items: Iterable[Term, Predicate], connective: Optional[Union[str, MathOperand]],
                 related_placeholder: AtomPlaceholder = None, parent: CNFFormula = None, scope: CNFFormula = None,
                 *args, **kwargs):
        super().__init__(items=items, related_placeholder=related_placeholder, parent=parent,
                         scope=scope, *args, **kwargs)

        if connective is None:
            self.connective = None
        elif isinstance(connective, str):
            try:
                self.connective = Atom.allowed_connective[connective]
            except KeyError:
                raise Exception(f'atom does not support connective \'{connective}\'')
        elif isinstance(connective, MathOperand):
            self.connective = connective
        else:
            raise TypeError(f'invalid argument type for field connective: {connective}')

    def __hash__(self):
        return hash(self.connective) ^ PredicateContainer.__hash__(self)

    def __eq__(self, other):
        if isinstance(other, Atom):
            return self.connective == other.connective and PredicateContainer.__eq__(self, other)
        raise NotImplementedError

    def __str__(self):
        # handle incorrect arity vs len(self._items)
        if self.connective is None or self.connective.value == 1:
            return str(self._items[0]) if self._items else ''

        # default visualization
        if self.connective == MathOperand.EQUAL:
            return '(' + ' = '.join(str(i) for i in self._items) + ')'
        if self.connective == MathOperand.NOT_EQUAL:
            return '(' + ' != '.join(str(i) for i in self._items) + ')'

        raise Exception(f'{self.connective} does not have default visualization')

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
