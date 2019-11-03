from __future__ import annotations

from abc import ABC

from ._folelement import FOLElement


class Term(ABC, FOLElement):
    """Term is element of language

    """

    def __init__(self, name: str, *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Term):
            return self.name == other.name
        elif isinstance(other, FOLElement):
            return False
        return False

    def __str__(self):
        return self.name
