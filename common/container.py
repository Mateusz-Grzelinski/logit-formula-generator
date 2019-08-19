from __future__ import annotations
from typing import List, Any


class Container:
    def __init__(self, additional_containers: List[Container], items: List[Any] = None):
        self.additional_containers = additional_containers
        """For containers, that are not items"""
        self._items = items if items is not None else []
        """Item can be also a container"""
        for i in self._items:
            if not Container._type_check(i):
                raise TypeError(f'Container can not store this object: {i}')

    @staticmethod
    def _type_check(obj):
        """Only objects that passes this check can be stored in Container"""
        return True

    @property
    def _other_containers(self):
        return self.additional_containers + [i for i in self._items if isinstance(i, Container)]
