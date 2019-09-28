from abc import abstractmethod

from src.ast import AstElement


class Placeholder:
    @abstractmethod
    def instantiate(self) -> AstElement:
        raise NotImplementedError

    def __str__(self):
        super_str = super().__str__()
        return super_str if super_str.startswith('_') else '_' + super_str
