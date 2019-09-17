from __future__ import annotations

from abc import abstractmethod


class AstElement:
    def __init__(self, related_placeholder: Placeholder = None):
        self.related_placeholder = related_placeholder

    def __repr__(self):
        return str(self)

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass
