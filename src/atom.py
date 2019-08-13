import random
from typing import List, Optional, Set

from src.name import SequentialNameGenerator


class Atom:
    """In current implementation atom is predicate. Inside predicate are functors or variables
    Predicate is statement that returns true or false
    """

    def __init__(self, name: str, arguments: List[str] = None):
        self.name = name
        self.arguments: List[str] = [] if arguments is None else arguments

    @property
    def arity(self) -> int:
        return len(self.arguments)

    @property
    def functors(self) -> Set[str]:
        """Functor is predicate that returns term, in tptpt it can be used only inside another predicate
        functor has scope of one file (one formula), it can be imported

        For example: `cnf(name, axiom, p(f, f1(a), f2(a, a)), f1(A) ).` `f` if 0-arity functor, called constant functor,
        `f1` is 1-arity, `f2` is 2-arity, p is 4-arity predicate
        see tptp SYN005-1.010.p for reference
        """
        return set(arg for arg in self.arguments if arg.islower())

    @property
    def number_of_functors(self) -> int:
        return len(self.functors)

    @property
    def total_functors(self) -> List[str]:
        return list(arg for arg in self.arguments if arg.islower())

    @property
    def total_number_of_functors(self) -> int:
        return len(self.total_functors)

    @property
    def variables(self) -> Set[str]:
        return set(arg for arg in self.arguments if arg.isupper())

    @property
    def number_of_variables(self) -> int:
        return len(self.variables)

    @property
    def total_variables(self) -> List[str]:
        return list(arg for arg in self.arguments if arg.isupper())

    @property
    def total_number_of_variables(self) -> int:
        return len(self.total_variables)

    def is_functor(self, parent):
        # todo check type of parent
        raise NotImplemented

    def is_constant_functor(self, parent):
        raise NotImplemented

    def is_predicate(self, parent):
        raise NotImplemented

    def to_tptp(self) -> str:
        if self.arguments:
            return f'{self.name}({",".join(self.arguments)})'
        else:
            return f'{self.name}'

    def __hash__(self):
        return hash(i for i in [self.name, self.arguments])

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.name == other.name and self.arguments == other.arguments

    def __str__(self):
        return self.to_tptp()

    def __repr__(self):
        return str((self.name, self.arguments))


class SimpleAtomGenerator:
    def __init__(self, predicate_name: str = 'p', argument: Optional[str] = 'a'):
        self.predicate_name_generator = SequentialNameGenerator(name=predicate_name)
        self.argument_generator = None if argument is None else SequentialNameGenerator(name=argument)
        self.generated_predicates = 0

    @property
    def atom(self) -> Atom:
        self.generated_predicates += 1
        if self.argument_generator is None:
            pred = Atom(name=self.predicate_name_generator.name)
        else:
            pred = Atom(name=self.predicate_name_generator.name,
                        arguments=[self.argument_generator.name])
        return pred

    @property
    def new_atom(self) -> Atom:
        self.generated_predicates += 1
        if self.argument_generator is None:
            pred = Atom(name=self.predicate_name_generator.new_name)
        else:
            # can not be twice used_name
            i = random.randint(0, 2)
            if i == 0:
                pred = Atom(name=self.predicate_name_generator.new_name,
                            arguments=[self.argument_generator.name])
            elif i == 1:
                pred = Atom(name=self.predicate_name_generator.name,
                            arguments=[self.argument_generator.new_name])
            elif i == 2:
                pred = Atom(name=self.predicate_name_generator.new_name,
                            arguments=[self.argument_generator.new_name])
            else:
                assert False
        return pred

    @property
    def used_predicate(self) -> Atom:
        if self.generated_predicates == 0:
            return self.new_atom
        self.generated_predicates += 1
        if self.argument_generator is None:
            pred = Atom(name=self.predicate_name_generator.used_name)
        else:
            pred = Atom(name=self.predicate_name_generator.used_name,
                        arguments=[self.argument_generator.used_name])
        return pred


class SafetyGenerator(SimpleAtomGenerator):

    def __init__(self, predicate_name: str = 'p', argument: str = 'A'):
        super().__init__(predicate_name, argument.upper())


class LivenessGenerator(SimpleAtomGenerator):
    def __init__(self, predicate_name: str = 'p', argument: str = 'a'):
        super().__init__(predicate_name, argument.lower())


class ConstantGenerator(SimpleAtomGenerator):

    def __init__(self, predicate_name: str = 'p'):
        super().__init__(predicate_name, None)


if __name__ == '__main__':
    p = Atom('p', arguments=['a', 'A'])
    p.functors
    p.total_functors
    p.total_number_of_functors
    p.number_of_functors
    p.variables
    p.arity
