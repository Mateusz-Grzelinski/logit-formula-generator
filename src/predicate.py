import random
from typing import List, Optional

from src.name import SequentialNameGenerator


class Predicate:
    def __init__(self, name: str, arguments: List[str] = None):
        self.name = name
        self.arguments: List[str] = [] if arguments is None else arguments

    @property
    def arity(self) -> int:
        return len(self.arguments)

    def to_tptp(self):
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


class SimplePredicateGenerator:
    def __init__(self, predicate_name: str = 'p', argument: Optional[str] = 'a'):
        self.predicate_name_generator = SequentialNameGenerator(name=predicate_name)
        self.argument_generator = None if argument is None else SequentialNameGenerator(name=argument)
        self.generated_predicates = 0

    @property
    def predicate(self) -> Predicate:
        self.generated_predicates += 1
        if self.argument_generator is None:
            pred = Predicate(name=self.predicate_name_generator.name)
        else:
            pred = Predicate(name=self.predicate_name_generator.name,
                             arguments=[self.argument_generator.name])
        return pred

    @property
    def new_predicate(self) -> Predicate:
        self.generated_predicates += 1
        if self.argument_generator is None:
            pred = Predicate(name=self.predicate_name_generator.new_name)
        else:
            # can not be twice used_name
            i = random.randint(0, 2)
            if i == 0:
                pred = Predicate(name=self.predicate_name_generator.new_name,
                                 arguments=[self.argument_generator.name])
            elif i == 1:
                pred = Predicate(name=self.predicate_name_generator.name,
                                 arguments=[self.argument_generator.new_name])
            elif i == 2:
                pred = Predicate(name=self.predicate_name_generator.new_name,
                                 arguments=[self.argument_generator.new_name])
            else:
                assert False
        return pred

    @property
    def used_predicate(self) -> Predicate:
        if self.generated_predicates == 0:
            return self.new_predicate
        self.generated_predicates += 1
        if self.argument_generator is None:
            pred = Predicate(name=self.predicate_name_generator.used_name)
        else:
            pred = Predicate(name=self.predicate_name_generator.used_name,
                             arguments=[self.argument_generator.used_name])
        return pred


class SafetyGenerator(SimplePredicateGenerator):

    def __init__(self, predicate_name: str = 'p', argument: str = 'A'):
        super().__init__(predicate_name, argument.upper())


class LivenessGenerator(SimplePredicateGenerator):
    def __init__(self, predicate_name: str = 'p', argument: str = 'a'):
        super().__init__(predicate_name, argument.lower())


class ConstantGenerator(SimplePredicateGenerator):

    def __init__(self, predicate_name: str = 'p'):
        super().__init__(predicate_name, None)
