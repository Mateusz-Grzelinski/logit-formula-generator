from __future__ import annotations

from typing import List, Optional, Union

from ast import Term, Variable, Functor, Predicate, Atom, CNFClause, CNFFormula, Literal
from ast.operands import MathOperand


class Placeholder:
    pass


class TermPlaceholder(Placeholder, Term):
    pass


class VariablePlaceholder(TermPlaceholder, Variable):
    def __init__(self, name: str = 'v'):
        super().__init__(name)


class FunctorPlaceholder(TermPlaceholder, Functor):
    def __init__(self, name: str = 'f', terms: List[Term] = None):
        super().__init__(name, terms)


class PredicatePlaceholder(Placeholder, Predicate):
    def __init__(self, name: str = 'p', terms: List[Term] = None):
        super().__init__(name, terms)


class AtomPlaceholder(Placeholder, Atom):
    def __init__(self, connective: Optional[Union[str, MathOperand]] = '',
                 arguments: List[Union[Term, Predicate]] = None):
        Placeholder.__init__(self)
        Atom.__init__(self, connective=connective, arguments=arguments)


class LiteralPlaceholder(Placeholder, Literal):
    def __init__(self, atom: Atom = None, negated: bool = False):
        super().__init__(atom, negated)


class CNFClausePlaceholder(Placeholder, CNFClause):
    pass


class CNFFormulaPlaceholder(Placeholder, CNFFormula):
    pass
