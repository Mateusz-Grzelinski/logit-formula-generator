from src.ast._connectives import TLConnective
from src.ast.temporal_logic import TLElement


class RelationalVariable(TLElement):
    def __init__(self, name: str, tl_connective: TLConnective, *args, **kwargs):
        super().__init__(unary_connective=[tl_connective], *args, **kwargs)
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, PropositionalVariable):
            return self.name == other.name
        raise NotImplementedError
