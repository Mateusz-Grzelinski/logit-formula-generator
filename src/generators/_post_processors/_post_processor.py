from __future__ import annotations

from abc import abstractmethod


class PostProcessor:

    @abstractmethod
    def post_process(self, formula: AstElement):
        """Post process formula"""
        pass
