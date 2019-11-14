from typing import Generator

from src.ast.first_order_logic import Atom, Variable
from src.generators._signatures.first_order_logic import AtomSignatureGenerator
from test.test_signatues.mock_signature_generators.mock_predicate_signature_generator import pred_func0_var, \
    pred_var_func1


class MockAtomSignatureGenerator(AtomSignatureGenerator):
    def __init__(self):
        super().__init__(connectives={'', '='}, predicate_gen=None, random=True)

    def generate(self) -> Generator[Atom, None, None]:
        global atom0, atom1, atom0_1
        yield atom0
        yield atom1
        yield atom0_1


atom0 = Atom(items=[pred_func0_var], connective='')
atom1 = Atom(items=[pred_var_func1], connective='')
atom0_1 = Atom(items=[Variable(name=AtomSignatureGenerator.variable_name), pred_var_func1], connective='=')
