from __future__ import annotations

from src.container import ConstantLengthContainer
from .ast_element import AstElement
from .atom import Atom
from .containers import AtomContainer


class Literal(AtomContainer, AstElement, container_implementation=ConstantLengthContainer):
    def __init__(self, item: Atom, negated: bool, related_placeholder: LiteralPlaceholder = None, *args, **kwargs):
        self.is_negated = negated
        super().__init__(items=[item], related_placeholder=related_placeholder, *args, **kwargs)

    def __hash__(self):
        return hash(self.is_negated) + super().__hash__()

    def __eq__(self, other):
        if isinstance(other, Literal):
            return self.is_negated == other.is_negated and super().__eq__(other)
        return False

    @property
    def atom(self):
        assert len(self._items) == 1, 'literal can have only one atom'
        return self._items[0]

    def __str__(self):
        if self.is_negated:
            return '~' + str(self.atom[0])

        return str(self.atom)
