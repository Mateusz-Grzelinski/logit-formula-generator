from __future__ import annotations

from src.containers import ConstantLengthContainer
from src.containers.fol import AtomContainer
from .atom import Atom
from .folelement import FolElement


class Literal(AtomContainer, FolElement, container_implementation=ConstantLengthContainer):
    def __init__(self, item: Atom, negated: bool, related_placeholder: LiteralPlaceholder = None,
                 parent: CNFFormula = None, scope: CNFFormula = None, *args, **kwargs):
        self.is_negated = negated
        super().__init__(items=[item], related_placeholder=related_placeholder, parent=parent, scope=scope, *args,
                         **kwargs)

    def __hash__(self):
        return hash(self.is_negated) + super().__hash__()

    def __eq__(self, other):
        if isinstance(other, Literal):
            return self.is_negated == other.is_negated and super().__eq__(other)
        return False

    def __str__(self):
        if self.is_negated:
            return '~' + str(self.atom)
        return str(self.atom)

    @property
    def atom(self):
        assert len(self._items) == 1, 'literal can have only one atom'
        return self._items[0]

    def update_scope(self):
        from src.ast.fol import CNFFormula
        parent = self.parent
        while parent is not None:
            if isinstance(parent, CNFFormula):
                self.scope = parent
                break
            parent = parent.parent
