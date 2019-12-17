from copy import deepcopy

from src.ast.first_order_logic import Functor, Variable
from src.generators._signatures.first_order_logic import FunctorGenerator


class TestFunctorSignatureGenerator:
    def test_functor_max_recursion_depth_0_arity_empty(self):
        # todo probably should raise some exception in this case....
        fg = FunctorGenerator(arities={}, max_recursion_depth=0, random=True)
        functors = list(fg.generate())
        assert functors == []

    def test_functor_max_recursion_depth_0_arity_0(self):
        fg = FunctorGenerator(arities={0}, max_recursion_depth=0, random=True)
        functors = list(fg.generate())
        assert Functor(name=fg.functor_name, items=[]) in functors
        assert len(functors) == 1

    def test_functor_max_recursion_depth_0_arity_1(self):
        fg = FunctorGenerator(arities={1}, max_recursion_depth=0, random=True)
        functors = list(fg.generate())
        assert Functor(name=fg.functor_name, items=[Variable(name=fg.variable_initial_name)]) in functors
        assert len(functors) == 1

    def test_functor_max_recursion_depth_0_arity_2(self):
        fg = FunctorGenerator(arities={2}, max_recursion_depth=0, random=True)
        functors = list(fg.generate())
        assert Functor(name=fg.functor_name,
                       items=[Variable(name=fg.variable_initial_name),
                              Variable(name=fg.variable_initial_name)]) in functors
        assert len(functors) == 1

    def test_change_in_variable_name_affects_only_one_variable(self):
        fg = FunctorGenerator(arities={2}, max_recursion_depth=0, random=True)
        functors = list(fg.generate())
        functor = functors[0]
        functor._items[0].name = 'V2'
        assert functor._items[0].name == 'V2' and functor._items[1].name == fg.variable_initial_name

    def test_functor_recursion_depth_0_multiple_arities(self):
        fg = FunctorGenerator(arities={0, 1, 2}, max_recursion_depth=0, random=True)
        functors = list(fg.generate())
        assert Functor(name=fg.functor_name, items=[]) in functors
        assert Functor(name=fg.functor_name, items=[Variable(name=fg.variable_initial_name)]) in functors
        assert Functor(name=fg.functor_name,
                       items=[Variable(name=fg.variable_initial_name),
                              Variable(name=fg.variable_initial_name)]) in functors
        assert len(functors) == 3

    def test_functor_recursion_depth_1_arity_0(self):
        # todo probably should raise some exception in this case....
        fg = FunctorGenerator(arities={}, max_recursion_depth=1, random=True)
        functors = list(fg.generate())
        assert functors == []

    def test_functor_recursion_depth_1_arity_1(self):
        # todo probably should raise some exception in this case....
        fg = FunctorGenerator(arities={1}, max_recursion_depth=1, random=True)
        functors = list(fg.generate())
        func_non_rec = Functor(name=fg.functor_name, items=[Variable(name=fg.variable_initial_name)])
        func_rec = Functor(name=fg.functor_name, items=[deepcopy(func_non_rec)])
        assert func_non_rec in functors
        assert func_rec in functors
        assert len(functors) == 2

    def test_change_in_functor_name_affects_only_one_functor(self):
        fg = FunctorGenerator(arities={1}, max_recursion_depth=1, random=True)
        functors = list(fg.generate())
        func_non_rec = Functor(name=fg.functor_name, items=[Variable(name=fg.variable_initial_name)])
        func_rec = Functor(name=fg.functor_name, items=[deepcopy(func_non_rec)])
        index = functors.index(func_non_rec)
        functors[index].name = 'f1'
        func_non_rec.name = 'f1'
        assert func_non_rec in functors
        assert func_rec in functors
        assert len(functors) == 2

    def test_functor_recursion_depth_2_arity_1(self):
        # todo probably should raise some exception in this case....
        fg = FunctorGenerator(arities={1}, max_recursion_depth=2, random=True)
        functors = list(fg.generate())
        func_non_rec = Functor(name=fg.functor_name, items=[Variable(name=fg.variable_initial_name)])
        func_rec_1 = Functor(name=fg.functor_name, items=[deepcopy(func_non_rec)])
        func_rec_2 = Functor(name=fg.functor_name, items=[deepcopy(func_rec_1)])
        assert func_non_rec in functors
        assert func_rec_1 in functors
        assert func_rec_2 in functors
        assert len(functors) == 3
