from __future__ import annotations

from abc import abstractmethod


class AstElement:
    def __init__(self, parent: AstElement = None, scope: AstElement = None, *args, **kwargs):
        self.scope = scope
        self.parent = parent
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return str(self)

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    @abstractmethod
    def update_scope(self):
        raise NotImplementedError
