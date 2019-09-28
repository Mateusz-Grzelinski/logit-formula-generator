from collections import MutableSequence
from typing import Iterable, overload

from .container import _ContainerBase, ItemType


class MutableContainer(_ContainerBase, MutableSequence):

    @overload
    def __setitem__(self, i: int, o: ItemType) -> None:
        ...

    @overload
    def __setitem__(self, i: slice, o: ItemType) -> None:
        ...

    def __setitem__(self, i: int, o: ItemType) -> None:
        self._items[i] = o

    @overload
    def __delitem__(self, i: int) -> None:
        ...

    @overload
    def __delitem__(self, i: slice) -> None:
        ...

    def __delitem__(self, i: int) -> None:
        del self._items[i]

    def __hash__(self):
        raise NotImplemented('Can not hash mutable containers')

    def __eq__(self, other):
        raise NotImplemented('Can not compare mutable containers')

    def _init_items(self, items: Iterable[ItemType]):
        return list(items) if items is not None else []

    def insert(self, index: int, object: ItemType) -> None:
        self._items.insert(index, object)
