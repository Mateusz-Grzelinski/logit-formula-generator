from __future__ import annotations
from typing import Union, List

from containers.container import Container
from containers.functor_container import FunctorContainer
from containers.variable_container import VariableContainer


class TermContainer(VariableContainer, FunctorContainer):
    @staticmethod
    def _type_check(obj):
        from ast.term import Term
        return isinstance(obj, Term)

    @property
    def terms(self):
        from ast.term import Term
        return (t for t in self._items if isinstance(t, Term))
