from __future__ import annotations

import io
from abc import abstractmethod, ABC


class Exporter(ABC):
    @abstractmethod
    def get_formula_as_string(self) -> io.StringIO:
        raise NotImplementedError


