from __future__ import annotations

from .folelement import FOLElement
from .term import Term


class Variable(Term, FOLElement):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        raise NotImplementedError
