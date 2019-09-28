from __future__ import annotations

from abc import ABC, abstractmethod
from collections import Sequence
from typing import Iterable, TypeVar, Generic, Tuple, overload, Union, List

ItemType = TypeVar('ItemType')


class _ContainerBase(Generic[ItemType], Sequence, ABC):
    """Private interface for containers implementations

    Lists all methods that implementations can provide. Depending on implementation some functionality will be disabled

    Possible implementations are: :class:`ImmutableContainer`, :class:`ConstantLengthContainer`, :class:`MutableContainer`
    """
    _implementation: Union[MutableContainer, ImmutableContainer, ConstantLengthContainer] = None

    def __init__(self, items: Sequence[ItemType], *args, **kwargs):
        self._items = self._init_items(items)

    @abstractmethod
    def _init_items(self, items: Iterable[ItemType]) -> List[ItemType]:
        return self._implementation._init_items(self, items=items)

    def __getitem__(self, i: int) -> ItemType:
        if isinstance(i, slice):
            raise NotImplementedError('Slicing is not supported')
        elif isinstance(i, int):
            return self._items[i]
        else:
            raise NotImplementedError('index must be integer')

    def __len__(self) -> int:
        return len(self._items)

    def __str__(self):
        return str(self._items)

    @abstractmethod
    def __hash__(self):
        return self._implementation.__hash__(self)

    @abstractmethod
    def __eq__(self, other):
        return self._implementation.__eq__(self, other)

    @abstractmethod
    def __setitem__(self, i: int, o: ItemType) -> None:
        return self._implementation.__setitem__(self, i, o)

    @abstractmethod
    def __delitem__(self, i: int) -> None:
        return self._implementation.__delitem__(self, i)

    @abstractmethod
    def insert(self, index: int, object: ItemType) -> None:
        return self._implementation.insert(self, index, object)

    @overload
    def items(self, enum: bool = False, include_nested: bool = True) -> Iterable[ItemType]:
        ...

    @overload
    def items(self, enum: bool = False, include_nested: bool = True) -> Iterable[Tuple[Container, int, ItemType]]:
        ...

    def items(self, enum: bool = False, include_nested: bool = True):
        # the order of 2 following loops is important
        # nested fol should be called first to fix with setting item to containers
        # but it is not optimal solution in terms of performance (recursion depth)
        if include_nested:
            for nested_container in self.nested_containers:
                yield from nested_container.items(enum=enum, include_nested=include_nested)
        if enum:
            for i, item in enumerate(self._items):
                yield self, i, item
        else:
            for item in self._items:
                yield item

    @property
    def nested_containers(self) -> Iterable[Container]:
        """iterate over all nested fol. Item can be a containers"""
        from .container import Container
        return (i for i in self._items if isinstance(i, Container))
