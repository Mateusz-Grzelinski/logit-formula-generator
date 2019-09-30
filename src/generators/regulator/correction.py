from dataclasses import field, dataclass
from enum import auto, Enum, unique

from .range import Range


@unique
class CorrectiveAction(Enum):
    GROW = auto()
    SHRINK = auto()
    NONE = auto()


@dataclass
class Correction:
    correction_range: Range = field(default_factory=Range)
    action: CorrectiveAction = CorrectiveAction.NONE
