from __future__ import annotations

from abc import abstractmethod
from typing import Iterable


class AstElement:
    def __init__(self, unary_connectives: Iterable[str, ConnectiveEnum, ConnectiveProperties] = None, *args, **kwargs):
        from ._connectives import ConnectiveProperties, ConnectiveEnum, get_connective_properties
        unary_connectives = [] if unary_connectives is None else unary_connectives
        self.unary_connective = []
        for unary_connective in unary_connectives:
            if isinstance(unary_connective, ConnectiveEnum) or isinstance(unary_connective, str):
                self.unary_connective.append(get_connective_properties(unary_connective))
            elif isinstance(unary_connective, ConnectiveProperties):
                self.unary_connective.append(unary_connective)
            else:
                assert False, f'Unknown {unary_connective} type'
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return str(self)

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    def _accept(self, visitor: AstVisitor):
        from ._containers import Container
        visitor.visit(self)
        if isinstance(self, Container):
            for item in self._items:
                item._accept(visitor)
