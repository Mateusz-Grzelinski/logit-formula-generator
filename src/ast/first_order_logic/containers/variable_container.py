from __future__ import annotations

from typing import Generator, overload, Iterable, Tuple, Type, Set

from src.ast.containers import Container


class VariableContainer(Container):
    def __init__(self, items: Iterable[Variable], *args, **kwargs):
        super().__init__(items=items, *args, **kwargs)

    @classmethod
    def contains(cls) -> Set[Type]:
        from src.ast.first_order_logic import Variable
        return {Variable}

    @overload
    def variables(self, enum: bool = True) -> Iterable[Tuple[Container, int, Variable]]:
        ...

    @overload
    def variables(self, enum: bool = False) -> Iterable[Variable]:
        ...

    def variables(self, enum: bool = False) -> Generator:
        from src.ast.first_order_logic.variable import Variable
        if enum:
            return ((container, i, v) for container, i, v in self.items(enum=True) if isinstance(v, Variable))
        else:
            return (v for v in self.items() if isinstance(v, Variable))

    @property
    def number_of_variables(self) -> int:
        return len(set(self.variables()))

    @property
    def number_of_variable_instances(self) -> int:
        return len(list(self.variables()))
