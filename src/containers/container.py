from __future__ import annotations

from abc import abstractmethod
from typing import Sequence

from ._containerbase import ItemType
from .immutablecontainer import ImmutableContainer


class Container(ImmutableContainer):
    """Public interface for containers"""

    def __init__(self, items: Sequence[ItemType], *args, **kwargs):
        super().__init__(items, *args, **kwargs)

    @classmethod
    @abstractmethod
    def contains(cls):
        raise NotImplementedError

