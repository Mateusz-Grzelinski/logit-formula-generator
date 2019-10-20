from collections import Hashable
from typing import Iterable, Tuple

from ._containerbase import _ContainerBase, ItemType


class ImmutableContainer(_ContainerBase, Hashable):
    def __hash__(self):
        return hash(self._items)

    def __eq__(self, other):
        if isinstance(other, ImmutableContainer):
            return self._items == other._items
        raise NotImplemented

    def __setitem__(self, i: int, o: ItemType) -> None:
        raise NotImplementedError('Cannot set item in immutable containers')

    def __delitem__(self, i: int) -> None:
        raise NotImplementedError('Cannot delete item in immutable containers')

    def _init_items(self, items: Iterable[ItemType]) -> Tuple[ItemType]:
        return tuple(items) if items is not None else ()

    def insert(self, index: int, object: ItemType) -> None:
        raise NotImplementedError('Cannot insert item to immutable containers')