from __future__ import annotations


class Term:
    """Term is element of language

    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return str(self)

