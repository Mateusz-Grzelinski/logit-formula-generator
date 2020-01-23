from typing import Generator

from src.generators._signatures.first_order_logic import AtomGenerator

from src.syntax_tree.first_order_logic import Atom, Variable
from test.test_signatues.mock_signature_generators.mock_predicate_signature_generator import pred_func0_var, \
    pred_var_func1


class MockAtomGenerator(AtomGenerator):
    def __init__(self):
        super().__init__(connectives={'', '='}, predicate_gen=None, random=True)

    def generate(self) -> Generator[Atom, None, None]:
        global atom0, atom1, atom0_1
        yield atom0
        yield atom1
        yield atom0_1


atom0 = Atom(children=[pred_func0_var], math_connective='')
atom1 = Atom(children=[pred_var_func1], math_connective='')
atom0_1 = Atom(children=[Variable(name=AtomGenerator.variable_name), pred_var_func1], math_connective='=')
