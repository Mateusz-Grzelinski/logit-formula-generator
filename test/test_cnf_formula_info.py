import src.ast.first_order_logic as fol


class TestFOLInfo:
    def test_one_variable_one_atom_one_clause(self):
        v = fol.Variable('V')
        a = fol.Atom(items=[v], connective=None)
        l = fol.Literal(items=a, negated=False)
        c = fol.CNFClause(items=[l])
        f = fol.CNFFormula(items=[c])

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

        assert info.number_of_instances[fol.Variable] == 1
        assert info.number_of_instances[fol.Predicate] == 0
        assert info.number_of_instances[fol.Functor] == 0
        assert info.number_of_instances[fol.Atom] == 1
        assert info.number_of_instances[fol.Literal] == 1
        assert info.number_of_instances[fol.CNFClause] == 1
        assert info.number_of_instances[fol.CNFFormula] == 1

        assert info.number_of[fol.Variable] == 1
        assert info.number_of[fol.Predicate] == 0
        assert info.number_of[fol.Functor] == 0
        assert info.number_of[fol.Atom] == 1
        assert info.number_of[fol.Literal] == 1
        assert info.number_of[fol.CNFClause] == 1
        assert info.number_of[fol.CNFFormula] == 1

    def test_two_variable_two_atom_one_clause(self):
        v1 = fol.Variable('V1')
        v2 = fol.Variable('V2')
        a1 = fol.Atom(items=[v1], connective=None)
        a2 = fol.Atom(items=[v2], connective=None)
        l1 = fol.Literal(items=a1, negated=False)
        l2 = fol.Literal(items=a2, negated=False)
        c = fol.CNFClause(items=[l1, l2])
        f = fol.CNFFormula(items=[c])

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

        assert info.number_of_instances[fol.Variable] == 2
        assert info.number_of_instances[fol.Predicate] == 0
        assert info.number_of_instances[fol.Functor] == 0
        assert info.number_of_instances[fol.Atom] == 2
        assert info.number_of_instances[fol.Literal] == 2
        assert info.number_of_instances[fol.CNFClause] == 1
        assert info.number_of_instances[fol.CNFFormula] == 1

        assert info.number_of[fol.Variable] == 2
        assert info.number_of[fol.Predicate] == 0
        assert info.number_of[fol.Functor] == 0
        assert info.number_of[fol.Atom] == 2
        assert info.number_of[fol.Literal] == 2
        assert info.number_of[fol.CNFClause] == 1
        assert info.number_of[fol.CNFFormula] == 1

    def test_two_variable_two_atom_two_clauses(self):
        v1 = fol.Variable('V1')
        v2 = fol.Variable('V2')
        a1 = fol.Atom(items=[v1], connective=None)
        a2 = fol.Atom(items=[v2], connective=None)
        l1 = fol.Literal(items=a1, negated=False)
        l2 = fol.Literal(items=a2, negated=False)
        c1 = fol.CNFClause(items=[l1])
        c2 = fol.CNFClause(items=[l2])
        f = fol.CNFFormula(items=[c1, c2])

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

        assert info.number_of_instances[fol.Variable] == 2
        assert info.number_of_instances[fol.Predicate] == 0
        assert info.number_of_instances[fol.Functor] == 0
        assert info.number_of_instances[fol.Atom] == 2
        assert info.number_of_instances[fol.Literal] == 2
        assert info.number_of_instances[fol.CNFClause] == 2
        assert info.number_of_instances[fol.CNFFormula] == 1

        assert info.number_of[fol.Variable] == 2
        assert info.number_of[fol.Predicate] == 0
        assert info.number_of[fol.Functor] == 0
        assert info.number_of[fol.Atom] == 2
        assert info.number_of[fol.Literal] == 2
        # clauses are equivalent in mathematical sense
        assert info.number_of[fol.CNFClause] == 2  # todo check: 1 or 2
        assert info.number_of[fol.CNFFormula] == 1

    def test_two_variable_two_predicate_two_atom_two_clauses(self):
        v1 = fol.Variable('V1')
        v2 = fol.Variable('V2')
        p1 = fol.Predicate('p1', items=[v1])
        p1_2 = fol.Predicate('p1', items=[v2])
        a1 = fol.Atom(items=[p1], connective=None)
        a2 = fol.Atom(items=[p1_2], connective=None)
        l1 = fol.Literal(items=a1, negated=False)
        l2 = fol.Literal(items=a2, negated=False)
        c1 = fol.CNFClause(items=[l1, l2])
        c2 = fol.CNFClause(items=[l2])
        f = fol.CNFFormula(items=[c1, c2])

        info = f.get_info()

        assert info.number_of_singleton_variables == 3
        assert info.number_of_equality_atom_instances == 0
        assert info.number_of_negated_literal_instances == 0
        assert info.clause_lengths[1] == 1
        assert info.clause_lengths[2] == 1
        assert len(info.clause_lengths) == 2
        assert info.number_of_horn_clauses_instances == 1
        assert info.predicate_arities[1] == 3
        assert len(info.predicate_arities) == 1
        assert info.functor_arities == {}
        assert info.term_instances_depths == {}

        assert info.number_of_instances[fol.Variable] == 3
        assert info.number_of_instances[fol.Predicate] == 3
        assert info.number_of_instances[fol.Functor] == 0
        assert info.number_of_instances[fol.Atom] == 3
        assert info.number_of_instances[fol.Literal] == 3
        assert info.number_of_instances[fol.CNFClause] == 2
        assert info.number_of_instances[fol.CNFFormula] == 1

        assert info.number_of[fol.Variable] == 3
        assert info.number_of[fol.Predicate] == 1
        assert info.number_of[fol.Functor] == 0
        assert info.number_of[fol.Atom] == 3
        assert info.number_of[fol.Literal] == 3
        # clauses are equivalent in mathematical sense
        assert info.number_of[fol.CNFClause] == 2
        assert info.number_of[fol.CNFFormula] == 1
