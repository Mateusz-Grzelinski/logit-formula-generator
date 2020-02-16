from src.generators._signatures.first_order_logic import AtomGenerator

from src.syntax_tree.first_order_logic import Variable, Atom
from test.test_signatues.mock_signature_generators.mock_predicate_signature_generator import \
    MockPredicateGenerator, pred_var, pred_var_func1, pred_func0_var


class TestAtomSignatureGenerator:
    def test_atom_connective_empty(self):
        ag = AtomGenerator(connectives={}, predicate_gen=MockPredicateGenerator())
        atoms = list(ag.generate)
        assert atoms == []

    def test_atom_connective_none(self):
        ag = AtomGenerator(connectives={''}, predicate_gen=MockPredicateGenerator())
        atoms = list(ag.generate)
        assert Atom(children=[Variable(name=ag.variable_name)], math_connective='') in atoms
        assert Atom(children=[pred_var], math_connective='') in atoms
        assert Atom(children=[pred_var_func1], math_connective='') in atoms
        assert Atom(children=[pred_func0_var], math_connective='') in atoms
        assert len(atoms) == 4
