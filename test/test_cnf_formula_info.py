import src.ast.first_order_logic as fof


class TestFOLInfo:
    def test_one_variable_one_atom_one_clause(self):
        v = fof.Variable('V')
        a = fof.Atom(items=[v], connective=None)
        l = fof.Literal(items=a, negated=False)
        c = fof.CNFClause(items=[l])
        f = fof.CNFFormula(items=[c])

        info = f.get_info()

        assert info.number_of_singleton_variables == 1
        assert info.number_of_equality_atom_instances == 0
        assert info.number_of_negated_literal_instances == 0
        assert info.clause_lengths[1] == 1
        assert len(info.clause_lengths) == 1
        assert info.number_of_horn_clauses_instances == 1
        assert info.predicate_arities == {}
        assert info.functor_arities == {}
        assert info.term_instances_depths == {}

        assert info.number_of_instances[fof.Variable] == 1
        assert info.number_of_instances[fof.Predicate] == 0
        assert info.number_of_instances[fof.Functor] == 0
        assert info.number_of_instances[fof.Atom] == 1
        assert info.number_of_instances[fof.Literal] == 1
        assert info.number_of_instances[fof.CNFClause] == 1
        assert info.number_of_instances[fof.CNFFormula] == 1

        assert info.number_of[fof.Variable] == 1
        assert info.number_of[fof.Predicate] == 0
        assert info.number_of[fof.Functor] == 0
        assert info.number_of[fof.Atom] == 1
        assert info.number_of[fof.Literal] == 1
        assert info.number_of[fof.CNFClause] == 1
        assert info.number_of[fof.CNFFormula] == 1

    def test_two_variable_two_atom_one_clause(self):
        v1 = fof.Variable('V1')
        v2 = fof.Variable('V2')
        a1 = fof.Atom(items=[v1], connective=None)
        a2 = fof.Atom(items=[v2], connective=None)
        l1 = fof.Literal(items=a1, negated=False)
        l2 = fof.Literal(items=a2, negated=False)
        c = fof.CNFClause(items=[l1, l2])
        f = fof.CNFFormula(items=[c])

        info = f.get_info()

        assert info.number_of_singleton_variables == 2
        assert info.number_of_equality_atom_instances == 0
        assert info.number_of_negated_literal_instances == 0
        assert info.clause_lengths[2] == 1
        assert len(info.clause_lengths) == 1
        assert info.number_of_horn_clauses_instances == 0
        assert info.predicate_arities == {}
        assert info.functor_arities == {}
        assert info.term_instances_depths == {}

        assert info.number_of_instances[fof.Variable] == 2
        assert info.number_of_instances[fof.Predicate] == 0
        assert info.number_of_instances[fof.Functor] == 0
        assert info.number_of_instances[fof.Atom] == 2
        assert info.number_of_instances[fof.Literal] == 2
        assert info.number_of_instances[fof.CNFClause] == 1
        assert info.number_of_instances[fof.CNFFormula] == 1

        assert info.number_of[fof.Variable] == 2
        assert info.number_of[fof.Predicate] == 0
        assert info.number_of[fof.Functor] == 0
        assert info.number_of[fof.Atom] == 2
        assert info.number_of[fof.Literal] == 2
        assert info.number_of[fof.CNFClause] == 1
        assert info.number_of[fof.CNFFormula] == 1

    def test_two_variable_two_atom_two_clauses(self):
        v1 = fof.Variable('V')
        v2 = fof.Variable('V')
        a1 = fof.Atom(items=[v1], connective=None)
        a2 = fof.Atom(items=[v2], connective=None)
        l1 = fof.Literal(items=a1, negated=False)
        l2 = fof.Literal(items=a2, negated=False)
        c1 = fof.CNFClause(items=[l1])
        c2 = fof.CNFClause(items=[l1])
        f = fof.CNFFormula(items=[c1, c2])

        info = f.get_info()

        assert info.number_of_singleton_variables == 2
        assert info.number_of_equality_atom_instances == 0
        assert info.number_of_negated_literal_instances == 0
        assert info.clause_lengths[1] == 2
        assert len(info.clause_lengths) == 1
        assert info.number_of_horn_clauses_instances == 2
        assert info.predicate_arities == {}
        assert info.functor_arities == {}
        assert info.term_instances_depths == {}

        assert info.number_of_instances[fof.Variable] == 2
        assert info.number_of_instances[fof.Predicate] == 0
        assert info.number_of_instances[fof.Functor] == 0
        assert info.number_of_instances[fof.Atom] == 2
        assert info.number_of_instances[fof.Literal] == 2
        assert info.number_of_instances[fof.CNFClause] == 2
        assert info.number_of_instances[fof.CNFFormula] == 1

        assert info.number_of[fof.Variable] == 2
        assert info.number_of[fof.Predicate] == 0
        assert info.number_of[fof.Functor] == 0
        assert info.number_of[fof.Atom] == 2
        assert info.number_of[fof.Literal] == 2
        # clauses are equivalent in mathematical sense
        assert info.number_of[fof.CNFClause] == 1
        assert info.number_of[fof.CNFFormula] == 1
