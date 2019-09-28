from collections import Hashable
from typing import Iterable, Tuple

from src.container.container import _ContainerBase, ItemType, Container


class ImmutableContainer(_ContainerBase, Hashable):
    def __hash__(self):
        return hash(self._items)

    def __eq__(self, other):
        from src.container.constantlengthcontainer import ConstantLengthContainer
        if isinstance(other, Container):
            if issubclass(other.implementation, ConstantLengthContainer):
                return NotImplemented('TODO')
            elif issubclass(other.implementation, ImmutableContainer):
                return self._items == other._items
        raise NotImplemented

    def __setitem__(self, i: int, o: ItemType) -> None:
        raise NotImplementedError('Cannot set item in immutable container')

    def __delitem__(self, i: int) -> None:
        raise NotImplementedError('Cannot delete item in immutable container')

    def _init_items(self, items: Iterable[ItemType]) -> Tuple[ItemType]:
        return tuple(items) if items is not None else ()

    def insert(self, index: int, object: ItemType) -> None:
        raise NotImplementedError('Cannot insert item to immutable container')
