from copy import deepcopy

from src.ast.first_order_logic import Variable, Predicate
from src.generators._signatures.first_order_logic import PredicateSignatureGenerator
from test.test_signatues.mock_signature_generators.mock_functor_signature_generator import \
    MockFunctorSignatureGenerator, func_rec_0, func_rec_1, func_rec_2


class TestPredicateSignatureGenerator:
    def test_predicate_arity_empty(self):
        # todo throw error?
        pg = PredicateSignatureGenerator(arities={}, functor_gen=MockFunctorSignatureGenerator())
        predicates = list(pg.generate())
        assert predicates == []

    def test_predicate_arity_0(self):
        pg = PredicateSignatureGenerator(arities={0}, functor_gen=MockFunctorSignatureGenerator())
        predicates = list(pg.generate())
        assert Predicate(name=pg.predicate_name, items=[]) in predicates
        assert len(predicates) == 1

    def test_predicate_arity_1(self):
        pg = PredicateSignatureGenerator(arities={1}, functor_gen=MockFunctorSignatureGenerator())
        predicates = list(pg.generate())
        assert Predicate(name=pg.predicate_name, items=[Variable(name=pg.variable_name)]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_0]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_1]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_2]) in predicates
        assert len(predicates) == 4

    def test_predicate_arity_2(self):
        pg = PredicateSignatureGenerator(arities={2}, functor_gen=MockFunctorSignatureGenerator())
        predicates = list(pg.generate())
        assert Predicate(name=pg.predicate_name, items=[Variable(name=pg.variable_name), func_rec_0]) in predicates
        assert Predicate(name=pg.predicate_name, items=[Variable(name=pg.variable_name), func_rec_1]) in predicates
        assert Predicate(name=pg.predicate_name, items=[Variable(name=pg.variable_name), func_rec_2]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_0, Variable(name=pg.variable_name)]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_1, Variable(name=pg.variable_name)]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_2, Variable(name=pg.variable_name)]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_0, func_rec_0]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_1, func_rec_0]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_2, func_rec_0]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_0, func_rec_1]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_1, func_rec_1]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_2, func_rec_1]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_0, func_rec_2]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_1, func_rec_2]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_2, func_rec_2]) in predicates
        assert len(predicates) == 16

    def test_change_in_functor_name_affects_one_functor(self):
        pg = PredicateSignatureGenerator(arities={2}, functor_gen=MockFunctorSignatureGenerator())
        predicates = list(pg.generate())

        p = Predicate(name=pg.predicate_name, items=[deepcopy(func_rec_1), deepcopy(func_rec_0)])
        index = predicates.index(p)
        predicates[index]._items[0].name = 'f1'
        p._items[0].name = 'f1'

        assert Predicate(name=pg.predicate_name, items=[Variable(name=pg.variable_name), func_rec_0]) in predicates
        assert Predicate(name=pg.predicate_name, items=[Variable(name=pg.variable_name), func_rec_1]) in predicates
        assert Predicate(name=pg.predicate_name, items=[Variable(name=pg.variable_name), func_rec_2]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_0, Variable(name=pg.variable_name)]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_1, Variable(name=pg.variable_name)]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_2, Variable(name=pg.variable_name)]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_0, func_rec_0]) in predicates
        assert p in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_2, func_rec_0]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_0, func_rec_1]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_1, func_rec_1]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_2, func_rec_1]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_0, func_rec_2]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_1, func_rec_2]) in predicates
        assert Predicate(name=pg.predicate_name, items=[func_rec_2, func_rec_2]) in predicates
        assert len(predicates) == 16
