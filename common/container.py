from __future__ import annotations

import itertools
from typing import List, Any, Iterable, NoReturn


class Container:
    def __init__(self, additional_containers: List[Container], items: List[Any] = None):
        self.additional_containers = additional_containers if additional_containers is not None else []
        """For containers, that are not items"""
        self._items = items if items is not None else []
        """Item can be also a container"""
        for i in self._items:
            if not Container._item_type_check(i):
                raise TypeError(f'Container can not store this object: {i}')

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

    def items(self, enum: bool = False):
        if enum:
            for i, item in enumerate(self._items):
                yield self, i, item
            for nested_container in self._nested_containers:
                yield from nested_container.items(enum=True)
        else:
            for item in self._items:
                yield item
            for nested_container in self._nested_containers:
                yield from nested_container.items()

    def __setitem__(self, key, value):
        self._items[key] = value

    def set_items(self, value: List[Any]) -> NoReturn:
        self._items = list(value)


if __name__ == '__main__':
    c = Container([], items=[1, 2, 3, 4, 5])
    c2 = Container([], items=[c, 7, 8, 9, 10])
    for container, i, item in c2.items(enum=True):
        # container[i] = item + 1
        print(f'{container=}, {i=}, {item=}')
    print(f'{c2._items=}')
