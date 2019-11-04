from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Iterable, TypeVar, Generic, Tuple, overload, List, Type

ItemType = TypeVar('ItemType')


class _ContainerBase(Generic[ItemType], Sequence, ABC):
    """Private interface for _containers implementations

    Lists all methods that implementations can provide. Depending on implementation some functionality will be disabled

    Possible implementations are: :class:`ImmutableContainer`, :class:`ConstantLengthContainer`, :class:`MutableContainer`
    """

    def __init__(self, items: Sequence[ItemType], *args, **kwargs):
        self._items = self._init_items(items)
        super().__init__(*args, **kwargs)

    @abstractmethod
    def _init_items(self, items: Iterable[ItemType]) -> List[ItemType]:
        raise NotImplementedError

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
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __setitem__(self, i: int, o: ItemType) -> None:
        raise NotImplementedError

    @abstractmethod
    def __delitem__(self, i: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def insert(self, index: int, object: ItemType) -> None:
        raise NotImplementedError

    @overload
    def items(self, type: Type = object, enum: bool = False, include_nested: bool = True) -> Iterable[
        Tuple[Container, int, ItemType]]:
        ...

    def items(self, type: Type = object, enum: bool = False, include_nested: bool = True) -> Iterable[ItemType]:
        # the order of 2 following loops is important
        # nested first_order_logic should be called first to fix with setting item to _containers
        # but it is not optimal solution in terms of performance (recursion depth)
        if include_nested:
            for nested_container in self.nested_containers:
                yield from nested_container.items(type=type, enum=enum, include_nested=include_nested)
        if enum:
            yield from ((self, i, item) for i, item in enumerate(self._items) if isinstance(item, type))
        else:
            yield from (item for item in self._items if isinstance(item, type))

    def number_of_instances(self, type: Type):
        return len(list(self.items(type=type)))

    @property
    def nested_containers(self) -> Iterable[Container]:
        """iterate over all nested first_order_logic. Item can be a _containers"""
        from .container import Container
        return (i for i in self._items if isinstance(i, Container))
