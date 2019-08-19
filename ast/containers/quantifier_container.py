from ast.containers import AtomContainer


class QuantifierContainer(AtomContainer):
    @staticmethod
    def _type_check(obj):
        from ast.quantifier import Quantifier
        return isinstance(obj, Quantifier)
