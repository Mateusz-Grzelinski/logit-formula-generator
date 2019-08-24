from __future__ import annotations

from typing import Set

from .containers import AtomContainer
from .containers import QuantifierContainer


class FOFFormula(AtomContainer, QuantifierContainer):
    allowed_connectives: Set[str] = {
        # unary:
        '~',
        # assoc
        '|', '&',
        # non assoc
        '<=>', '=>', '<=', '<~>', '~|', '~&',
        # quantifiers: ! - for all, ? - exists
        '!', '?'
    }
    # fof_term: List[Union[Atom, Quantifier]]
