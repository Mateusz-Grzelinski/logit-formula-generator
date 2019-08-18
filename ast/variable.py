from __future__ import annotations
from ast.term import Term


class Variable(Term):
    def __init__(self, name: str):
        super().__init__(name.capitalize())

