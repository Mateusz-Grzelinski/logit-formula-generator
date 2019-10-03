from typing import Iterable

from src.ast.first_order_logic.containers.atom_container import AtomContainer
from src.ast.first_order_logic.containers.quantifier_container import QuantifierContainer
from src.ast.operands import LogicalConnective


class FolFormulae(AtomContainer, QuantifierContainer):

    def __init__(self, connectives: Iterable[str, LogicalConnective], items: Iterable[Atom], *args, **kwargs):
        super().__init__(items, *args, **kwargs)
        self.connectives = connectives
