from ast.atom import Atom
from ast.containers import AtomContainer
from ast.operands import LogicalOperand


class Literal(AtomContainer):
    def __init__(self, atom: Atom, negated: bool):
        self.operand = LogicalOperand.NOT if negated else None
        super().__init__(additional_containers=[], items=[atom])

    @property
    def atom(self):
        assert len(self._items) == 1, 'literal can have only one atom'
        return self._items[0]

    def __str__(self):
        if self.operand:
            return '~' + str(self.atom)

        return str(self.atom)
