from abc import ABC
from typing import Iterable

from src.ast.first_order_logic.containers.fol_formulae_container import FolFormulaeContainer
from src.ast.first_order_logic.folelement import FolElement


class Quantifier(FolElement, FolFormulaeContainer, ABC):
    def __init__(self, variable_list: Iterable[Variable], items: Iterable[Predicate, Functor], *args, **kwargs):
        super().__init__(parent=None, scope=None, items=items, *args, **kwargs)
        self.variable_list = variable_list

    def __hash__(self):
        pass

    def __eq__(self, other):
        pass

    def update_scope(self):
        pass


class ExistentialQuantifier(Quantifier):
    pass


class UniversalQuantifier(Quantifier):
    pass
