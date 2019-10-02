from __future__ import annotations

from abc import abstractmethod
from typing import Iterable, Type, Sequence

from ._containerbase import _ContainerBase, ItemType


class Container(_ContainerBase):
    """Public interface for containers"""

    def __init__(self, items: Sequence[ItemType], *args, **kwargs):
        super().__init__(items, *args, **kwargs)

    def _init_items(self, items: Iterable[ItemType]):
        return super()._init_items(items=items)

    def __init_subclass__(cls, *, container_implementation: Type[_ContainerBase] = None, **kwargs):
        assert issubclass(cls, Container)
        assert container_implementation is not None, 'You must provide implementation'
        assert issubclass(container_implementation, _ContainerBase), 'Implementation must derive _ContainerBase'
        cls._implementation = container_implementation

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        return super().__eq__(other)

    def __setitem__(self, i: int, o: ItemType) -> None:
        return super().__setitem__(i, o)

    def __delitem__(self, i: int) -> None:
        return super().__delitem__(i)

    def insert(self, index: int, object: ItemType) -> None:
        return super().insert(index, object)

    @classmethod
    @abstractmethod
    def contains(cls):
        raise NotImplementedError

    @classmethod
    def implementation(cls) -> Type:
        return cls._implementation
