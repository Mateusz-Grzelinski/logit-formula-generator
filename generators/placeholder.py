from __future__ import annotations

from abc import abstractmethod, ABC
from typing import List, Optional, Union

from ast import Term, Variable, Functor, Predicate, Atom, CNFClause, CNFFormula, Literal, AstElement
from ast.operands import MathOperand


class Placeholder:
    @abstractmethod
    def instantiate(self) -> AstElement:
        pass


class TermPlaceholder(Placeholder, Term, ABC):
    pass


class VariablePlaceholder(TermPlaceholder, Variable):
    def __init__(self, name: str = 'v'):
        super().__init__(name)

    def instantiate(self) -> Variable:
        return Variable(name=self.name)


class FunctorPlaceholder(TermPlaceholder, Functor):
    def __init__(self, name: str = 'f', terms: List[Term] = None):
        super().__init__(name, terms)

    def __hash__(self):
        return hash(self.name) + hash(tuple(self.items()))

    def instantiate(self) -> Functor:
        terms = []
        for item in self.items():
            if isinstance(item, Placeholder):
                terms.append(item.instantiate())
            else:
                terms.append(item)
        return Functor(name=self.name, terms=terms)


class PredicatePlaceholder(Placeholder, Predicate):
    def __init__(self, name: str = 'p', terms: List[Term] = None):
        super().__init__(name, terms)

    def instantiate(self) -> Predicate:
        terms = []
        for item in self.items():
            if isinstance(item, Placeholder):
                terms.append(item.instantiate())
            else:
                terms.append(item)
        return Predicate(name=self.name, terms=terms)


class AtomPlaceholder(Placeholder, Atom):
    def __init__(self, connective: Optional[Union[str, MathOperand]] = '',
                 arguments: List[Union[Term, Predicate]] = None):
        Placeholder.__init__(self)
        Atom.__init__(self, connective=connective, arguments=arguments)

    def instantiate(self) -> Atom:
        arguments = []
        for item in self.items():
            if isinstance(item, Placeholder):
                arguments.append(item.instantiate())
            else:
                arguments.append(item)
        return Atom(connective=self.connective, arguments=arguments)


class LiteralPlaceholder(Placeholder, Literal):
    def __init__(self, atom: Atom = None, negated: bool = False):
        super().__init__(atom, negated)

    def instantiate(self) -> Literal:
        if isinstance(self.atom, Placeholder):
            return Literal(atom=self.atom.instantiate(), negated=self.is_negated)
        else:
            return Literal(atom=self.atom, negated=self.is_negated)


class CNFClausePlaceholder(Placeholder, CNFClause):
    def instantiate(self) -> CNFClause:
        literals = []
        for item in self.items():
            if isinstance(item, Placeholder):
                literals.append(item.instantiate())
            else:
                literals.append(item)
        return CNFClause(literals=literals)


class CNFFormulaPlaceholder(Placeholder, CNFFormula):
    pass
