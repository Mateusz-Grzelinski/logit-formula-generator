import random
from abc import abstractmethod
from typing import List

from src._common import random_bool


class NameGenerator:

    def __iter__(self):
        while True:
            yield self.name

    @property
    @abstractmethod
    def generated_names(self) -> int:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def new_name(self) -> str:
        pass

    @property
    @abstractmethod
    def used_name(self) -> str:
        pass


class SequentialNameGenerator(NameGenerator):
    """Generates exactly total_literals literals by appending number to name
    generator is depleted when self.literals_left == 0
    """

    def __init__(self, name: str = 'p'):
        """
        :param name: prefix of literal
        """
        self._name = name
        self._literal_number = 0

    @property
    def generated_names(self) -> int:
        return self._literal_number

    @property
    def name(self) -> str:
        return self.used_name if random_bool() else self.new_name

    @property
    def used_name(self) -> str:
        if self._literal_number == 0:
            return self.new_name

        return f'{self._name}{random.randint(0, self._literal_number - 1)}'

    @property
    def new_name(self) -> str:
        self._literal_number += 1
        return f'{self._name}{self._literal_number}'


class NamePicker(NameGenerator):

    def __init__(self, names: List[str]):
        self.literals = names
        self._generated_literals = 0
        self.generated_indexes = set()

    @property
    def generated_names(self) -> int:
        return self._generated_literals

    @property
    def name(self) -> str:
        if len(self.generated_indexes) < len(self.literals):
            return self.used_name if random_bool() else self.new_name
        else:
            return self.used_name

    @property
    def new_name(self) -> str:
        if len(self.generated_indexes) == len(self.literals):
            return self.used_name
        self._generated_literals += 1

        while True:
            index = random.randint(0, len(self.literals))
            if index not in self.generated_indexes:
                self.generated_indexes.add(index)
                return self.literals[index]

    @property
    def used_name(self) -> str:
        if not self.generated_indexes:
            return self.new_name
        self._generated_literals += 1
        index = random.choice(tuple(self.generated_indexes))
        return self.literals[index]
