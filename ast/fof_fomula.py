from __future__ import annotations


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
