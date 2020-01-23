import src.syntax_tree.first_order_logic as fol


class TestFOLInfo:
    def test_one_variable_one_atom_one_clause(self):
        v = fol.Variable('V')
        a = fol.Atom(children=[v], math_connective=None)
        l = fol.Literal(children=a, negated=False)
        c = fol.CNFClause(children=[l])
        f = fol.CNFFOLFormula(children=[c])

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
        assert info.number_of_instances[fol.CNFFOLFormula] == 1

        assert info.number_of[fol.Variable] == 1
        assert info.number_of[fol.Predicate] == 0
        assert info.number_of[fol.Functor] == 0
        assert info.number_of[fol.Atom] == 1
        assert info.number_of[fol.Literal] == 1
        assert info.number_of[fol.CNFClause] == 1
        assert info.number_of[fol.CNFFOLFormula] == 1

    def test_two_variable_two_atom_one_clause(self):
        v1 = fol.Variable('V1')
        v2 = fol.Variable('V2')
        a1 = fol.Atom(children=[v1], math_connective=None)
        a2 = fol.Atom(children=[v2], math_connective=None)
        l1 = fol.Literal(children=a1, negated=False)
        l2 = fol.Literal(children=a2, negated=False)
        c = fol.CNFClause(children=[l1, l2])
        f = fol.CNFFOLFormula(children=[c])

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
        assert info.number_of_instances[fol.CNFFOLFormula] == 1

        assert info.number_of[fol.Variable] == 2
        assert info.number_of[fol.Predicate] == 0
        assert info.number_of[fol.Functor] == 0
        assert info.number_of[fol.Atom] == 2
        assert info.number_of[fol.Literal] == 2
        assert info.number_of[fol.CNFClause] == 1
        assert info.number_of[fol.CNFFOLFormula] == 1

    def test_two_variable_two_atom_two_clauses(self):
        v1 = fol.Variable('V1')
        v2 = fol.Variable('V2')
        a1 = fol.Atom(children=[v1], math_connective=None)
        a2 = fol.Atom(children=[v2], math_connective=None)
        l1 = fol.Literal(children=a1, negated=False)
        l2 = fol.Literal(children=a2, negated=False)
        c1 = fol.CNFClause(children=[l1])
        c2 = fol.CNFClause(children=[l2])
        f = fol.CNFFOLFormula(children=[c1, c2])

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
        assert info.number_of_instances[fol.CNFFOLFormula] == 1

        assert info.number_of[fol.Variable] == 2
        assert info.number_of[fol.Predicate] == 0
        assert info.number_of[fol.Functor] == 0
        assert info.number_of[fol.Atom] == 2
        assert info.number_of[fol.Literal] == 2
        # clauses are equivalent in mathematical sense
        assert info.number_of[fol.CNFClause] == 2  # todo check: 1 or 2
        assert info.number_of[fol.CNFFOLFormula] == 1

    def test_two_variable_two_predicate_two_atom_two_clauses(self):
        v1 = fol.Variable('V1')
        v2 = fol.Variable('V2')
        p1 = fol.Predicate('p1', children=[v1])
        p1_2 = fol.Predicate('p1', children=[v2])
        a1 = fol.Atom(children=[p1], math_connective=None)
        a2 = fol.Atom(children=[p1_2], math_connective=None)
        l1 = fol.Literal(children=a1, negated=False)
        l2 = fol.Literal(children=a2, negated=False)
        c1 = fol.CNFClause(children=[l1, l2])
        c2 = fol.CNFClause(children=[l2])
        f = fol.CNFFOLFormula(children=[c1, c2])

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
        assert info.number_of_instances[fol.CNFFOLFormula] == 1

        assert info.number_of[fol.Variable] == 3
        assert info.number_of[fol.Predicate] == 1
        assert info.number_of[fol.Functor] == 0
        assert info.number_of[fol.Atom] == 3
        assert info.number_of[fol.Literal] == 3
        # clauses are equivalent in mathematical sense
        assert info.number_of[fol.CNFClause] == 2
        assert info.number_of[fol.CNFFOLFormula] == 1

    def test_two_predicate_one_functor_two_atom_two_clauses(self):
        p1 = fol.Predicate('p1', children=[])
        f1 = fol.Functor('f1', children=[])
        p2 = fol.Predicate('p1', children=[f1])
        a1 = fol.Atom(children=[p1], math_connective=None)
        a2 = fol.Atom(children=[p2], math_connective=None)
        l1 = fol.Literal(children=a1, negated=False)
        l2 = fol.Literal(children=a2, negated=False)
        c1 = fol.CNFClause(children=[l1, l2])
        c2 = fol.CNFClause(children=[l2])
        f = fol.CNFFOLFormula(children=[c1, c2])

        info = f.get_info()

        assert info.number_of_singleton_variables == 0
        assert info.number_of_equality_atom_instances == 0
        assert info.number_of_negated_literal_instances == 0
        assert info.clause_lengths[1] == 1
        assert info.clause_lengths[2] == 1
        assert len(info.clause_lengths) == 2
        assert info.number_of_horn_clauses_instances == 1
        assert info.predicate_arities[0] == 1
        assert info.predicate_arities[1] == 2
        assert len(info.predicate_arities) == 2
        assert info.functor_arities[0] == 2
        assert len(info.functor_arities) == 1
        assert info.term_instances_depths[0] == 2
        assert len(info.term_instances_depths) == 1

        assert info.number_of_instances[fol.Variable] == 0
        assert info.number_of_instances[fol.Predicate] == 3
        assert info.number_of_instances[fol.Functor] == 2
        assert info.number_of_instances[fol.Atom] == 3
        assert info.number_of_instances[fol.Literal] == 3
        assert info.number_of_instances[fol.CNFClause] == 2
        assert info.number_of_instances[fol.CNFFOLFormula] == 1

        assert info.number_of[fol.Variable] == 0
        assert info.number_of[fol.Predicate] == 2
        assert info.number_of[fol.Functor] == 1
        assert info.number_of[fol.Atom] == 2
        assert info.number_of[fol.Literal] == 2
        # clauses are equivalent in mathematical sense
        assert info.number_of[fol.CNFClause] == 2
        assert info.number_of[fol.CNFFOLFormula] == 1
