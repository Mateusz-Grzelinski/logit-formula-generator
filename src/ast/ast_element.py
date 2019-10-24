from __future__ import annotations

from abc import abstractmethod

from src.ast.containers import Container


class AstElement:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return str(self)

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    def _accept(self, visitor: Visitor):
        visitor.visit(self)
        if isinstance(self, Container):
            for item in self._items:
                item._accept(visitor)
