from __future__ import annotations
from typing import List, Generator

from containers.container import Container


class VariableContainer(Container):
    @staticmethod
    def _type_check(obj):
        from ast.variable import Variable
        return isinstance(obj, Variable)

    @property
    def variables(self) -> Generator:
        from ast.variable import Variable
        return (v for v in self._items if isinstance(v, Variable))

    @property
    def number_of_variables(self):
        return len(set(self.variables)) + \
               sum(len(set(v_cont.variables)) for v_cont in self._other_containers if isinstance(v_cont, VariableContainer))