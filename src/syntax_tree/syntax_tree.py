from __future__ import annotations

from abc import ABC
from collections.abc import MutableSequence
from typing import Iterable, TypeVar, overload, Tuple

ChildrenType = TypeVar('ChildrenType')


# class SyntaxTreeNode(ABC):
#     def __init__(self, unary_connectives: Iterable[str, ConnectiveEnum, ConnectiveProperties] = None, *args, **kwargs):
#         from .connectives import ConnectiveProperties, ConnectiveEnum, get_connective_properties
#         unary_connectives = [] if unary_connectives is None else unary_connectives
#         self.unary_connectives = []
#         for unary_connective in unary_connectives:
#             if isinstance(unary_connective, ConnectiveEnum) or isinstance(unary_connective, str):
#                 self.unary_connectives.append(get_connective_properties(unary_connective))
#             elif isinstance(unary_connective, ConnectiveProperties):
#                 self.unary_connectives.append(unary_connective)
#             else:
#                 assert False, f'Unknown {unary_connective} type'
#         super().__init__(*args, **kwargs)
#
#     def _accept(self, visitor: AstVisitor):
#         visitor.visit(self)


class SyntaxTreeNode(MutableSequence, ABC):
    def __init__(self, children: MutableSequence[ChildrenType]):
        self._children = list(children)
        super().__init__()

    def __getitem__(self, i: int) -> ChildrenType:
        return self._children[i]

    def __len__(self) -> int:
        return len(self._children)

    def __str__(self) -> str:
        return str(self._children)

    def __hash__(self) -> int:
        # this is not safe nor efficient...
        return hash(tuple(i for i in self._children))

    def __eq__(self, other):
        if isinstance(other, SyntaxTreeNode):
            return len(self) == len(other) and all(i == j for i, j in zip(self._children, other._children))
        raise NotImplementedError

    def __setitem__(self, i: int, o: ChildrenType) -> None:
        self._children[i] = o

    def __delitem__(self, i: int) -> None:
        del self._children[i]

    def insert(self, index: int, object: ChildrenType) -> None:
        self._children.insert(index, object)

    @overload
    def recursive_nodes(self, type: ChildrenType = object, enum: bool = True) -> Iterable[
        Tuple[SyntaxTreeNode, ChildrenType]]:
        ...

    def recursive_nodes(self, type: ChildrenType = object, enum: bool = False) -> Iterable[ChildrenType]:
        # the order of 2 following loops is important
        # nested first_order_logic should be called first to fix with setting item to _containers
        # but it is not optimal solution in terms of performance (recursion depth)
        for nested_container in self.nested_containers:
            yield from nested_container.recursive_nodes(type=type, enum=enum)
        if enum:
            yield from ((self, i, item) for i, item in enumerate(self._children) if isinstance(item, type))
        else:
            yield from (item for item in self._children if isinstance(item, type))

    @property
    def nested_containers(self) -> Iterable[SyntaxTreeNode]:
        """iterate over all nested first_order_logic. Item can be a _containers"""
        return (i for i in self._children if isinstance(i, SyntaxTreeNode))

    def _accept(self, visitor: AstVisitor):
        visitor.visit(self)
        if isinstance(self, SyntaxTreeNode):
            for item in self._children:
                item._accept(visitor)


class FirstOrderLogicNode(SyntaxTreeNode):
    pass


class TemporalLogicNode(SyntaxTreeNode):
    pass
