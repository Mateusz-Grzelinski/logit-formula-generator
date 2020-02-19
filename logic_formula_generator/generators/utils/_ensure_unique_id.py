from copy import deepcopy
from typing import Iterable, Sequence


def ensure_unique_id(items: Sequence) -> Iterable:
    for index, item in enumerate(items):
        if any(id(item) == id(_i) for _i in items[index:]):
            yield deepcopy(items[index])
        else:
            yield item
