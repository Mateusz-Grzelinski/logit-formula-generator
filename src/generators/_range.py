from __future__ import annotations

import math
from collections.abc import Sequence
from typing import overload


class IntegerRange(Sequence):
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

    @property
    def average(self):
        return (self.min + self.max) / 2

    @classmethod
    def from_relative(cls, number: int, threshold: float = None, min_delta: int = None) -> IntegerRange:
        if threshold is None and min_delta is None:
            raise AttributeError('one of threshold or delta must be defined')
        elif threshold is None:
            return cls(int(number - min_delta), int(number + min_delta))
        elif min_delta is None:
            delta_from_threshold = number * threshold
            return cls(int(number - delta_from_threshold), int(number + delta_from_threshold))
        else:
            delta_from_threshold = number * threshold
            return cls(min(int(number - delta_from_threshold), number - min_delta),
                       max(int(number + delta_from_threshold), number + min_delta))
