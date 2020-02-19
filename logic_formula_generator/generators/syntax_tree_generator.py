from __future__ import annotations

from abc import abstractmethod
from typing import Any, Generator

from logic_formula_generator.syntax_tree import SyntaxTreeNode


class SyntaxTreeGenerator:
    """Abstract syntax tree generator"""

    @abstractmethod
    def generate(self) -> Generator[SyntaxTreeNode, Any, Any]:
        pass
