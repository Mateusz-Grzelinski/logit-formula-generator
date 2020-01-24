from __future__ import annotations

import io
from abc import abstractmethod, ABC

from src.syntax_tree.propositional_temporal_logic.visitors.propositional_temporal_logic_visitor import \
    PropositionalTemporalLogicVisitor


class Exporter(ABC):
    @abstractmethod
    def get_formula_as_string(self) -> io.StringIO:
        raise NotImplementedError


class PropositionalTemporalLogicExporter(PropositionalTemporalLogicVisitor, Exporter):
    def get_formula_as_string(self) -> io.StringIO:
        raise NotImplementedError

