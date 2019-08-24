from __future__ import annotations

import itertools
from typing import List, Any


class Container:
    def __init__(self, additional_containers: List[Container], items: List[Any] = None):
        self.additional_containers = additional_containers
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
    def _all_containers(self):
        """iterate over all nested containers. Item can be a container"""
        return itertools.chain((i for i in self.additional_containers),
                               (i for i in self._items if isinstance(i, Container))
                               )

    @property
    def items(self):
        return self._items
