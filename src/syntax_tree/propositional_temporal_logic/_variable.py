from ..syntax_tree import TemporalLogicNode


class Variable(TemporalLogicNode):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        raise NotImplementedError

    def __str__(self):
        return ''.join(i.connective.value for i in self.unary_connectives if i.connective is not None) + self.name
