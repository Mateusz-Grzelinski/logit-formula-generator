from __future__ import annotations

from ..ast_element import AstElement


class FolElement(AstElement):
    def __init__(self, parent: AstElement = None, scope: AstElement = None,
                 *args, **kwargs):
        super().__init__(parent, scope, *args, **kwargs)
