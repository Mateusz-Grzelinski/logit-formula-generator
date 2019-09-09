from __future__ import annotations

from typing import Generator

from common.container import Container


class VariableContainer(Container):
    @staticmethod
    def _item_type_check(obj):
        from ast.variable import Variable
        return isinstance(obj, Variable)

    def variables(self, enum: bool = False) -> Generator:
        from ast.variable import Variable
        if enum:
            return ((container, i, v) for container, i, v in self.items(enum=True) if isinstance(v, Variable))
        else:
            return (v for v in self.items() if isinstance(v, Variable))

    @property
    def number_of_variables(self) -> int:
        # todo count variables per scope (clause, quantifier)
        return len(set(self.variables()))

    @property
    def number_of_variable_instances(self) -> int:
        # todo count variables per scope (clause, quantifier)
        return len(list(self.variables()))
