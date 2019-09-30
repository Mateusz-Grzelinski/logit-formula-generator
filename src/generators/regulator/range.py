import math
from collections.abc import Sequence
from typing import overload


class Range(Sequence):
    @overload
    def __getitem__(self, i: int) -> int:
        ...

    def __getitem__(self, i: int) -> int:
        if i == 0:
            return self.min
        elif i == 1:
            return self.max
        raise IndexError('Range has only index 0-min and 1-max')

    def __len__(self) -> int:
        return 2

    def __init__(self, min: int = -math.inf, max: int = math.inf):
        self.min: int = min
        self.max: int = max

    def __contains__(self, item: int):
        return self.min <= item <= self.max

    def __str__(self):
        return f'Range(min={self.min}, max={self.max})'

    def __repr__(self):
        return f'({self.min}, {self.max})'
