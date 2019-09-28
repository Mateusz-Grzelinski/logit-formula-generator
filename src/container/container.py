from __future__ import annotations

from abc import ABC, abstractmethod
from collections import Sequence
from typing import Iterable, TypeVar, Generic, Tuple, overload, Union, Type, List

ItemType = TypeVar('ItemType')


class _ContainerBase(Generic[ItemType], Sequence, ABC):
    """Private interface for container implementations

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

    def __repr__(self):
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
        # nested containers should be called first to fix with setting item to container
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
        """iterate over all nested containers. Item can be a container"""
        return (i for i in self._items if isinstance(i, Container))


class Container(_ContainerBase):
    """Public interface for container"""

    def _init_items(self, items: Iterable[ItemType]):
        return super()._init_items(items=items)

    # def __init__(self, items: Sequence[ItemType] = None, *args, **kwargs):
    #     self._implementation.__init__(self, items=items, *args, **kwargs)
    #     do not call super, implementation will initialize everything

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
    def implementation(cls) -> Type:
        return cls._implementation
