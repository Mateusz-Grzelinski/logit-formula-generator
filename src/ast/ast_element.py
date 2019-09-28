from __future__ import annotations

from abc import abstractmethod


class AstElement:
    def __init__(self, related_placeholder: Placeholder = None, parent: AstElement = None, scope: AstElement = None,
                 *args, **kwargs):
        self.scope = scope
        self.parent = parent
        self.related_placeholder = related_placeholder

    def __repr__(self):
        return str(self)

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def update_scope(self):
        raise NotImplementedError
