from __future__ import annotations

from abc import ABC

from .ast_element import AstElement


class Term(ABC, AstElement):
    """Term is element of language

    """

    def __init__(self, name: str):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Term):
            return self.name == other.name
        raise NotImplemented

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return str(self)

