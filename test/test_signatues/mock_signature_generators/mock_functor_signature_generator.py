from copy import deepcopy
from typing import Generator

from src.ast.first_order_logic import Functor, Variable
from src.generators._signatures.first_order_logic import FunctorSignatureGenerator


class MockFunctorSignatureGenerator(FunctorSignatureGenerator):
    def __init__(self):
        super().__init__(arities={1}, max_recursion_depth=2, random=True)

    def generate(self) -> Generator[Functor, None, None]:
        global func_rec_0, func_rec_1, func_rec_2
        yield func_rec_0
        yield func_rec_1
        yield func_rec_2


func_rec_0 = Functor(name=MockFunctorSignatureGenerator.functor_name,
                     items=[Variable(name=MockFunctorSignatureGenerator.variable_name)])
func_rec_1 = Functor(name=MockFunctorSignatureGenerator.functor_name, items=[deepcopy(func_rec_0)])
func_rec_2 = Functor(name=MockFunctorSignatureGenerator.functor_name, items=[deepcopy(func_rec_1)])
