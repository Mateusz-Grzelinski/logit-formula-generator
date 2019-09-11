from .ast_element import AstElement
from .atom import Atom
from .containers import AtomContainer


class Literal(AtomContainer, AstElement):
    def __init__(self, atom: Atom, negated: bool, mutable: bool = True):
        self.is_negated = negated
        super().__init__(additional_containers=[], items=[atom], mutable=mutable)

    @property
    def atom(self):
        assert len(self._items) == 1, 'literal can have only one atom'
        return self._items[0]

    def __str__(self):
        if self.is_negated:
            return '~' + str(self.atom)

        return str(self.atom)
