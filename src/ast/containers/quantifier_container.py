from __future__ import annotations

from src.ast.containers import AtomContainer


class QuantifierContainer(AtomContainer):
    @staticmethod
    def _item_type_check(obj):
        from src.ast.quantifier import Quantifier
        return isinstance(obj, Quantifier)
