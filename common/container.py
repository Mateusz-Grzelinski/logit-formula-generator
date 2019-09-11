from __future__ import annotations

import itertools
from typing import List, Any, Iterable, NoReturn


class Container:
    def __init__(self, additional_containers: Iterable[Container], items: Iterable[Any] = None, mutable: bool = True):
        self.additional_containers = list(additional_containers) if additional_containers is not None else []
        if mutable:
            self._items = list(items) if items is not None else []
        else:
            self._items = tuple(items) if items is not None else ()
        for i in self._items:
            if not Container._item_type_check(i):
                raise TypeError(f'Container can not store this object: {i}')

    @property
    def is_mutable(self):
        return isinstance(self._items, list)

    @staticmethod
    def _item_type_check(obj) -> bool:
        """Only objects that passes this check can be stored in Container"""
        return True

    @staticmethod
    def _container_type_check(cont) -> bool:
        return isinstance(cont, Container)

    @property
    def _nested_containers(self) -> Iterable:
        """iterate over all nested containers. Item can be a container"""
        return itertools.chain((i for i in self.additional_containers),
                               (i for i in self._items if isinstance(i, Container))
                               )

    def pop(self, index: int = -1):
        return self._items.pop(index)

    def items(self, enum: bool = False, include_nested: bool = True):
        if enum:
            # the order of 2 following loops is important
            # nested containers should be called first to fix with setting item to container
            # but it is not optimal solution in terms of performance (recursion depth)
            if include_nested:
                for nested_container in self._nested_containers:
                    yield from nested_container.items(enum=True, include_nested=include_nested)
            for i, item in enumerate(self._items):
                yield self, i, item
        else:
            if include_nested:
                for nested_container in self._nested_containers:
                    yield from nested_container.items(enum=enum, include_nested=include_nested)
            for item in self._items:
                yield item

    def __setitem__(self, key, value):
        self._items[key] = value

    def set_items(self, value: List[Any]) -> NoReturn:
        self._items = list(value)
