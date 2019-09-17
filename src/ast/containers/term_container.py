from __future__ import annotations

from .functor_container import FunctorContainer
from .variable_container import VariableContainer


class TermContainer(VariableContainer, FunctorContainer):
    @staticmethod
    def _item_type_check(obj):
        from src.ast.term import Term
        return isinstance(obj, Term)

    @property
    def terms(self, enum: bool = False):
        from src.ast.term import Term
        if enum:
            return ((container, i, t) for container, i, t in self.items(enum=True) if isinstance(t, Term))
        else:
            return (t for t in self.items() if isinstance(t, Term))
