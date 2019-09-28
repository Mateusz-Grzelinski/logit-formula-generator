from abc import ABC
from typing import Optional, Union, Iterable

from src.ast.fol import Term, Variable, Functor, Predicate, Atom, CNFClause, CNFFormula, Literal
from src.ast.operands import MathOperand
from src.containers import ImmutableContainer
from ...placeholders import Placeholder


class TermPlaceholder(Placeholder, Term, ABC):
    pass


class VariablePlaceholder(TermPlaceholder, Variable):
    def __init__(self, name: str = 'v'):
        super().__init__(name)

    def instantiate(self) -> Variable:
        return Variable(name=self.name, related_placeholder=self)


class FunctorPlaceholder(TermPlaceholder, Functor, container_implementation=ImmutableContainer):
    def __init__(self, name: str = '_f', items: Iterable[Term] = None):
        super().__init__(name=name, items=items)

    def __hash__(self):
        return hash(self.name) + hash(tuple(self.items()))

    def instantiate(self) -> Functor:
        terms = []
        for item in self._items:
            if isinstance(item, Placeholder):
                terms.append(item.instantiate())
            else:
                terms.append(item)
        return Functor(name=self.name, items=terms, related_placeholder=self)


class PredicatePlaceholder(Placeholder, Predicate, container_implementation=ImmutableContainer):
    def __init__(self, name: str = 'p', items: Iterable[Term] = None):
        super().__init__(name=name, items=items)

    def instantiate(self) -> Predicate:
        terms = []
        for item in self._items:
            if isinstance(item, Placeholder):
                terms.append(item.instantiate())
            else:
                terms.append(item)
        return Predicate(name=self.name, items=terms, related_placeholder=self)


class AtomPlaceholder(Placeholder, Atom, container_implementation=ImmutableContainer):
    def __init__(self, connective: Optional[Union[str, MathOperand]] = '',
                 items: Iterable[Union[Term, Predicate]] = None):
        super().__init__(connective=connective, items=items)

    def instantiate(self) -> Atom:
        arguments = []
        for item in self._items:
            if isinstance(item, Placeholder):
                arguments.append(item.instantiate())
            else:
                arguments.append(item)
        return Atom(connective=self.connective, items=arguments, related_placeholder=self)


class LiteralPlaceholder(Placeholder, Literal, container_implementation=ImmutableContainer):
    def __init__(self, item: Atom = None, negated: bool = False):
        item = AtomPlaceholder() if item is None else item
        super().__init__(item, negated)

    def instantiate(self) -> Literal:
        if isinstance(self.atom, AtomPlaceholder):
            return Literal(item=self.atom.instantiate(), negated=self.is_negated, related_placeholder=self)
        else:
            return Literal(item=self.atom, negated=self.is_negated, related_placeholder=self)


class CNFClausePlaceholder(Placeholder, CNFClause, container_implementation=ImmutableContainer):
    def __init__(self, items: Iterable[Literal] = None):
        super().__init__(items)

    def instantiate(self) -> CNFClause:
        literals = []
        for item in self._items:
            if isinstance(item, Placeholder):
                literals.append(item.instantiate())
            else:
                literals.append(item)
        return CNFClause(items=literals, related_placeholder=self)


class CNFFormulaPlaceholder(Placeholder, CNFFormula, container_implementation=ImmutableContainer):
    pass
