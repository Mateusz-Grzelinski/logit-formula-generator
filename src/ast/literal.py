from __future__ import annotations

from .ast_element import AstElement
from .atom import Atom
from .containers import AtomContainer


class Literal(AtomContainer, AstElement):
    def __init__(self, atom: Atom, negated: bool, mutable: bool = True, related_placeholder: LiteralPlaceholder = None):
        self.is_negated = negated
        super().__init__(additional_containers=[], items=[atom], mutable=mutable)
        AstElement.__init__(self, related_placeholder=related_placeholder)

    def __hash__(self):
        return hash(self.is_negated) + hash(self.atom)

    def __eq__(self, other):
        if isinstance(other, Literal):
            return self.is_negated == other.is_negated and self.atom == other.atom
        return False

    @property
    def atom(self):
        assert len(self._items) == 1, 'literal can have only one atom'
        return self._items[0]

    def __str__(self):
        if self.is_negated:
            return '~' + str(self.atom)

        return str(self.atom)
