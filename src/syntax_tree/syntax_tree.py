from __future__ import annotations

from abc import ABC
from collections.abc import MutableSequence
from typing import Iterable, TypeVar, overload, Tuple

from ..syntax_tree.syntax_tree_visitor import SyntaxTreeVisitor

ChildrenType = TypeVar('ChildrenType')


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

    def _accept(self, visitor: SyntaxTreeVisitor):
        visitor.visit_pre(self)
        # iterate all except last one to avoid last call on visitor.visit_in_between_children()
        for item in self[:-1]:
            item._accept(visitor)
            visitor.visit_in_between_children(self)
        if len(self):
            self[-1]._accept(visitor)
        visitor.visit_post(self)


class FirstOrderLogicNode(SyntaxTreeNode):
    pass


class TemporalLogicNode(SyntaxTreeNode):
    pass
