from __future__ import annotations

from abc import abstractmethod
from typing import Any, Generator


class AstGenerator:
    """Abstract syntax tree generator"""

    @abstractmethod
    def generate(self) -> Generator[AstElement, Any, Any]:
        pass
