from __future__ import annotations

from typing import Iterable

from src.ast.ast_element import AstElement
from src.containers import ConstantLengthContainer
from src.containers.fol import TermContainer
from .term import Term


class Functor(Term, TermContainer, AstElement, container_implementation=ConstantLengthContainer):
    def __init__(self, name: str, items: Iterable[Term] = None, related_placeholder: FunctorPlaceholder = None,
                 parent: CNFFormula = None, scope: CNFFormula = None, *args, **kwargs):
        super().__init__(name=name, items=items, related_placeholder=related_placeholder, parent=parent, scope=scope,
                         *args, **kwargs)

    def __hash__(self):
        return hash(self.name) + super().__hash__()

    def __eq__(self, other):
        if isinstance(other, Functor):
            return self.name == other.name and super().__eq__(other)
        raise NotImplementedError

    def __str__(self):
        if len(list(self._items)) != 0:
            return f'{self.name}({", ".join(str(t) for t in self._items)})'
        else:
            return f'{self.name}'

    @property
    def arity(self):
        return len(self.items())

    @property
    def is_recursive(self):
        return any(isinstance(t, Functor) for t in self.items())

    @property
    def recursion_depth(self):
        if self.is_recursive:
            return max(f.recursion_depth + 1 for f in self.functors())
        else:
            return 0

    @property
    def is_constant(self):
        return len(self._items) == 0

    def update_scope(self):
        from src.ast.fol import CNFFormula
        parent = self.parent
        while parent is not None:
            if isinstance(parent, CNFFormula):
                self.scope = parent
                break
            parent = parent.parent
