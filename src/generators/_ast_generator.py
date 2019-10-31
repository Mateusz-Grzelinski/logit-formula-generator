from abc import abstractmethod
from typing import Any, Generator


class AstGenerator:
    """Abstract syntax tree generator"""

    @abstractmethod
    def generate(self) -> Generator[Any, Any, Any]:
        pass
