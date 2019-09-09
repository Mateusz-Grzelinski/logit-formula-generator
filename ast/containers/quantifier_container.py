from __future__ import annotations

from ast.containers import AtomContainer


class QuantifierContainer(AtomContainer):
    @staticmethod
    def _item_type_check(obj):
        from ast.quantifier import Quantifier
        return isinstance(obj, Quantifier)
