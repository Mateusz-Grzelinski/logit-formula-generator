from __future__ import annotations

from .ast_element import AstElement
from .term import Term


class Variable(Term, AstElement):
    def __init__(self, name: str):
        super().__init__(name)
