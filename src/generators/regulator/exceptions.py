from __future__ import annotations

from typing import Type


class PropagateToParent(Exception):
    def __init__(self, *args: object, failing_ast_element: Type[AstElement], required_correction: Correction) -> None:
        super().__init__(*args)
        self.propagate_to = failing_ast_element
        self.required_correction = required_correction
