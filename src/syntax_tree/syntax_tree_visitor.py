from __future__ import annotations

from typing import NoReturn


class SyntaxTreeVisitor:
    def visit_pre(self, element: SyntaxTreeNode) -> NoReturn:
        pass

    def visit_post(self, element: SyntaxTreeNode) -> NoReturn:
        pass

    def visit_in_between_children(self, element: SyntaxTreeNode) -> NoReturn:
        pass
