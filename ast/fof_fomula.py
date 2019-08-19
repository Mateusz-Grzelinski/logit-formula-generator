from __future__ import annotations

from typing import Set

from containers.atom_container import AtomContainer
from containers.quantifier_container import QuantifierContainer


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
