from __future__ import annotations

import os
from abc import abstractmethod
from typing import NoReturn

from src.ast import AstVisitor


class Exporter(AstVisitor):
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    @abstractmethod
    def export(self, expression: CNFFormula, filename_suffix: str = '') -> NoReturn:
        raise NotImplementedError
