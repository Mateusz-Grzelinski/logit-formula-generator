from abc import abstractmethod


class AstElement:
    def __repr__(self):
        return str(self)

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass
