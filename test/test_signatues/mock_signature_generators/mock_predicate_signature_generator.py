from typing import Generator

from src.ast.first_order_logic import Predicate, Variable
from src.generators._signatures.first_order_logic import PredicateGenerator
from test.test_signatues.mock_signature_generators.mock_functor_signature_generator import func_rec_0, func_rec_1


class MockPredicateGenerator(PredicateGenerator):
    def __init__(self):
        super().__init__(arities={2}, functor_gen=None)

    def generate(self, random: bool = True) -> Generator[Predicate, None, None]:
        global pred_func0_var, pred_var_func1, pred_var
        yield pred_var
        yield pred_func0_var
        yield pred_var_func1


pred_var = Predicate(name=PredicateGenerator.predicate_name,
                     items=[Variable(name=PredicateGenerator.variable_name)])
pred_var_func1 = Predicate(name=PredicateGenerator.predicate_name,
                           items=[Variable(name=PredicateGenerator.variable_name), func_rec_1])
pred_func0_var = Predicate(name=PredicateGenerator.predicate_name,
                           items=[func_rec_0, Variable(name=PredicateGenerator.variable_name)])
