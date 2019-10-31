from __future__ import annotations

from abc import abstractmethod
from typing import Sequence, Any, Type, Set

from ._containerbase import ItemType
from .immutablecontainer import ImmutableContainer


class Container(ImmutableContainer):
    """Public interface for _containers"""

    def __init__(self, items: Sequence[ItemType], *args, **kwargs):
        super().__init__(items, *args, **kwargs)

    @classmethod
    @abstractmethod
    def contains(cls) -> Set[Type[Any]]:
        raise NotImplementedError
