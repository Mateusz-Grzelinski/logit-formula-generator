from __future__ import annotations

import itertools
from dataclasses import field, dataclass
from typing import TypeVar, Generic, List, Iterable, Generator

ValueType = TypeVar('ValueType')


@dataclass
class WeightedSequence(Generic[ValueType]):
    values: List[ValueType] = field(default_factory=list)
    weights: List[float] = field(default_factory=list)

    def to_weighted_values(self) -> Generator:
        for value, weight in itertools.zip_longest(self.values, self.weights):
            yield WeightedValue(value, weight)

    @classmethod
    def from_weighted_values(cls, weighted_values: Iterable[WeightedValue]):
        values = []
        weights = []
        for wv in weighted_values:
            values.append(wv.value)
            weights.append(wv.weight)
        return cls(values, weights)


@dataclass(repr=False, frozen=False)
class WeightedValue(Generic[ValueType]):
    value: ValueType = field(compare=True)
    weight: float = field(compare=False)

    def __str__(self):
        return str((self.value, self.weight))

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.value)
