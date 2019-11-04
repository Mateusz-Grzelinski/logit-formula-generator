from src.ast.temporal_logic.tl_element import TLElement


class PropositionalVariable(TLElement):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, PropositionalVariable):
            return self.name == other.name
        raise NotImplementedError
