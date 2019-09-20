from __future__ import annotations

from abc import abstractmethod, ABC
from typing import List, Optional, Union, Iterable

from src.ast import Term, Variable, Functor, Predicate, Atom, CNFClause, CNFFormula, Literal, AstElement
from src.ast.operands import MathOperand


class Placeholder:
    @abstractmethod
    def instantiate(self) -> AstElement:
        pass

    def __str__(self):
        super_str = super().__str__()
        return super_str if super_str.startswith('_') else '_' + super_str


class TermPlaceholder(Placeholder, Term, ABC):
    pass


class VariablePlaceholder(TermPlaceholder, Variable):
    def __init__(self, name: str = 'v'):
        super().__init__(name)

    def instantiate(self) -> Variable:
        return Variable(name=self.name, related_placeholder=self)


class FunctorPlaceholder(TermPlaceholder, Functor):
    def __init__(self, name: str = '_f', terms: Iterable[Term] = None):
        super().__init__(name=name, terms=terms, mutable=False)

    def __hash__(self):
        return hash(self.name) + hash(tuple(self.items()))

    def instantiate(self) -> Functor:
        terms = []
        for item in self._items:
            if isinstance(item, Placeholder):
                terms.append(item.instantiate())
            else:
                terms.append(item)
        return Functor(name=self.name, terms=terms, related_placeholder=self)


class PredicatePlaceholder(Placeholder, Predicate):
    def __init__(self, name: str = 'p', terms: Iterable[Term] = None):
        super().__init__(name=name, terms=terms, mutable=False)

    def instantiate(self) -> Predicate:
        terms = []
        for item in self._items:
            if isinstance(item, Placeholder):
                terms.append(item.instantiate())
            else:
                terms.append(item)
        return Predicate(name=self.name, terms=terms, related_placeholder=self)


class AtomPlaceholder(Placeholder, Atom):
    def __init__(self, connective: Optional[Union[str, MathOperand]] = '',
                 arguments: List[Union[Term, Predicate]] = None):
        super().__init__(connective=connective, arguments=arguments, mutable=False)

    def instantiate(self) -> Atom:
        arguments = []
        for item in self._items:
            if isinstance(item, Placeholder):
                arguments.append(item.instantiate())
            else:
                arguments.append(item)
        return Atom(connective=self.connective, arguments=arguments, related_placeholder=self)


class LiteralPlaceholder(Placeholder, Literal):
    def __init__(self, atom: Atom = None, negated: bool = False):
        atom = AtomPlaceholder() if atom is None else atom
        super().__init__(atom, negated, mutable=False)

    def instantiate(self) -> Literal:
        if isinstance(self.atom, AtomPlaceholder):
            return Literal(atom=self.atom.instantiate(), negated=self.is_negated, related_placeholder=self)
        else:
            return Literal(atom=self.atom, negated=self.is_negated, related_placeholder=self)


class CNFClausePlaceholder(Placeholder, CNFClause):
    def __init__(self, literals: List[Literal] = None):
        super().__init__(literals, mutable=False)

    def instantiate(self) -> CNFClause:
        literals = []
        for item in self._items:
            if isinstance(item, Placeholder):
                literals.append(item.instantiate())
            else:
                literals.append(item)
        return CNFClause(literals=literals, related_placeholder=self)


class CNFFormulaPlaceholder(Placeholder, CNFFormula):
    pass
