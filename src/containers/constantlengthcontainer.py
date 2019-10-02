from collections import Hashable
from typing import Iterable, List

from .container import _ContainerBase, ItemType, Container


class ConstantLengthContainer(_ContainerBase, Hashable):
    def __setitem__(self, key: int, value: ItemType):
        self._items[key] = value

    def __delitem__(self, i: int) -> None:
        raise NotImplementedError('Container can not change length')

    def __hash__(self):
        return hash(len(self._items))

    def __eq__(self, other):
        from .immutablecontainer import ImmutableContainer
        if isinstance(other, Container):
            if issubclass(other.implementation(), ConstantLengthContainer):
                return len(self._items) == len(other._items)
            elif issubclass(other.implementation(), ImmutableContainer):
                raise NotImplemented
        raise NotImplemented

    def __str__(self):
        return f'{repr(self)}/{len(self)}'

    def _init_items(self, items: Iterable[ItemType]) -> List[ItemType]:
        return list(items) if items is not None else []

    def insert(self, index: int, object: ItemType) -> None:
        raise NotImplementedError('Can not insert to constant length containers')
