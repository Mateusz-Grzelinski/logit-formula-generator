from __future__ import annotations

import io
import json
from abc import abstractmethod, ABC
from enum import Enum
from inspect import isclass

from src.syntax_tree.propositional_temporal_logic.visitors.propositional_temporal_logic_visitor import \
    PropositionalTemporalLogicVisitor


class Exporter(ABC):
    @abstractmethod
    def get_formula_as_string(self) -> io.StringIO:
        raise NotImplementedError


class PropositionalTemporalLogicExporter(PropositionalTemporalLogicVisitor, Exporter):
    def get_formula_as_string(self) -> io.StringIO:
        raise NotImplementedError


class SerializableJSONEncoder(json.JSONEncoder):
    """This encoder can encode Enum and classes that inherit Serializable
    Usage json.dumps(variable, cls=SerializableJSONEncoder)
    """

    def default(self, o):
        if isclass(o):
            return self._as_plain_dict(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

    def _as_plain_dict(self, o):
        """Convert to dict that holds only basic types"""
        # todo ignore variables that start with _
        class_dict = o.__dict__.copy()
        for key, value in o.__dict__.recursive_nodes():
            if key.startswith('_') or key.startswith(self.__class__.__name__):
                class_dict.pop(key)
                continue
            # recursion is not efficies, but is is easy
            if isclass(value):
                class_dict[key] = self._as_plain_dict(value)
        return class_dict
