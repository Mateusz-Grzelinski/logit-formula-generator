from ast.containers import AtomContainer


class LiteralContainer(AtomContainer):

    @staticmethod
    def _type_check(obj):
        from ast.literal import Literal
        return isinstance(obj, Literal)

    def literals(self):
        from ast.literal import Literal
        return (l for l in self._items if isinstance(l, Literal))
