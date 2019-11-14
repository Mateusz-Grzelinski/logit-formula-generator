from ._temporal_logic_element import TemporalLogicElement


class Variable(TemporalLogicElement):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        raise NotImplementedError
