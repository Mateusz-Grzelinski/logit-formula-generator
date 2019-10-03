from __future__ import annotations

from ..ast_element import AstElement


class FolElement(AstElement):
    def __init__(self, related_placeholder: Placeholder = None, parent: AstElement = None, scope: AstElement = None,
                 *args, **kwargs):
        super().__init__(related_placeholder, parent, scope, *args, **kwargs)
