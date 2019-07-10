import random
from abc import abstractmethod
from typing import Optional, List

from src._common import random_bool


class NameGenerator:

    def __iter__(self):
        while True:
            yield self.name

    @abstractmethod
    @property
    def generated_names(self) -> int:
        pass

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
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
    def name(self) -> Optional[str]:
        return self.used_name if random_bool() else self.new_name

    @property
    def used_name(self) -> Optional[str]:
        if self._literal_number == 0:
            return None

        return f'{self._name}{random.randint(0, self._literal_number - 1)}'

    @property
    def new_name(self) -> str:
        self._literal_number += 1
        return f'{self._name}{self._literal_number}'


class NamePicker(NameGenerator):

    def __init__(self, names: List[str]):
        self.literals = names
        self._generated_literals = 0

    @property
    def generated_names(self) -> int:
        return self._generated_literals

    @property
    def name(self) -> str:
        self._generated_literals += 1
        return random.choice(self.literals)
