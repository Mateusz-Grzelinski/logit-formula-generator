from __future__ import annotations

from typing import List, Optional, Union, Dict

from ast.containers import PredicateContainer
from ast.containers import TermContainer
from ast.operands import MathOperand
from ast.predicate import Predicate
from ast.term import Term


class Atom(TermContainer, PredicateContainer):
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

    def __init__(self, connective: Optional[Union[str, MathOperand]], arguments: List[Union[Term, Predicate]]):
        if isinstance(connective, str):
            try:
                self.connective = Atom.allowed_connective[connective]
            except KeyError:
                raise Exception(f'atom does not support connective \'{connective}\'')
        elif isinstance(connective, MathOperand):
            self.connective = connective
        else:
            raise TypeError(f'invalid argument type for field connective: {connective}')

        # todo arguments should be the same type? have the same return type
        # todo check number of arguments
        super().__init__(additional_containers=[], items=arguments)

    def __str__(self):
        # handle incorrect arity vs len(self._items)
        if self.connective is None or self.connective.value == 1:
            return str(self._items[0])

        # default visualization
        if self.connective == MathOperand.EQUAL:
            return '(' + ' = '.join(str(i) for i in self._items) + ')'
        if self.connective == MathOperand.NOT_EQUAL:
            return '(' + ' != '.join(str(i) for i in self._items) + ')'

        raise Exception(f'{self.connective} does not have default visualization')

    def __repr__(self) -> str:
        return str(self)
