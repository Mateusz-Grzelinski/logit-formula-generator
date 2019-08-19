from __future__ import annotations

from ast.containers import FunctorContainer
from ast.containers import VariableContainer


class TermContainer(VariableContainer, FunctorContainer):
    @staticmethod
    def _type_check(obj):
        from ast.term import Term
        return isinstance(obj, Term)

    @property
    def terms(self):
        from ast.term import Term
        return (t for t in self._items if isinstance(t, Term))
