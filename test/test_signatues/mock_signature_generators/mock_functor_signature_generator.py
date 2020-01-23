from copy import deepcopy
from typing import Generator

from src.generators._signatures.first_order_logic import FunctorGenerator

from src.syntax_tree.first_order_logic import Functor, Variable


class MockFunctorGenerator(FunctorGenerator):
    def __init__(self):
        super().__init__(arities={1}, max_recursion_depth=2, random=True)

    def generate(self) -> Generator[Functor, None, None]:
        global func_rec_0, func_rec_1, func_rec_2
        yield func_rec_0
        yield func_rec_1
        yield func_rec_2


func_rec_0 = Functor(name=MockFunctorGenerator.functor_name,
                     children=[Variable(name=MockFunctorGenerator.variable_initial_name)])
func_rec_1 = Functor(name=MockFunctorGenerator.functor_name, children=[deepcopy(func_rec_0)])
func_rec_2 = Functor(name=MockFunctorGenerator.functor_name, children=[deepcopy(func_rec_1)])
