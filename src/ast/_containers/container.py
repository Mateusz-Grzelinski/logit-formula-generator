from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import MutableSequence
from typing import Iterable, TypeVar, Generic, Tuple, overload, Type, Set, Any

ItemType = TypeVar('ItemType')


class Container(Generic[ItemType], MutableSequence, ABC):
    """Private interface for _containers implementations

    Lists all methods that implementations can provide. Depending on implementation some functionality will be disabled

    Possible implementations are: :class:`ImmutableContainer`, :class:`ConstantLengthContainer`, :class:`MutableContainer`
    """

    def __init__(self, items: MutableSequence[ItemType], *args, **kwargs):
        self._items = list(items)
        super().__init__(*args, **kwargs)

    def __getitem__(self, i: int) -> ItemType:
        return self._items[i]

    def __len__(self) -> int:
        return len(self._items)

    def __str__(self):
        return str(self._items)

    def __hash__(self):
        # this is not safe nor efficient...
        return hash(tuple(i for i in self._items))

    def __eq__(self, other):
        if isinstance(other, Container):
            return len(self) == len(other) and all(i == j for i, j in zip(self._items, other._items))
        raise NotImplementedError

    def __setitem__(self, i: int, o: ItemType) -> None:
        self._items[i] = o

    def __delitem__(self, i: int) -> None:
        del self._items[i]

    def insert(self, index: int, object: ItemType) -> None:
        self._items.insert(index, object)

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
        return (i for i in self._items if isinstance(i, Container))

    @classmethod
    @abstractmethod
    def contains(cls) -> Set[Type[Any]]:
        raise NotImplementedError
