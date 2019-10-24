from pprint import pprint
from typing import Iterable, Generator

import src.generators.signatures.first_order_logic as fof
from src.ast.first_order_logic import CNFFormula
from src.generators.post_processors.fol_post_processor import FOLPostProcessor
from src.generators.range import Range


class LivenessSafetyGenerator:
    def __init__(self, functor_arity: Iterable[int], predicate_arities: Iterable[int], connectives: Iterable[str],
                 clause_lengths: Iterable[int],
                 number_of_clauses: Range, number_of_literals: Range, predicate_names: Iterable[str],
                 functor_names: Iterable[str], variable_names: Iterable[str]):
        self.predicate_names = predicate_names
        self.functor_names = functor_names
        self.variable_names = variable_names
        self.number_of_literals = number_of_literals
        self.number_of_clauses = number_of_clauses
        self.clause_lengths = clause_lengths
        self.connectives = connectives
        self.predicate_arities = predicate_arities
        self.functor_arity = functor_arity

    def generate(self) -> Generator[CNFFormula, None, None]:
        f = fof.FunctorSignatureGenerator(arities=self.functor_arity, max_recursion_depth=0)
        print('functors:', end=' ')
        pprint(list(f.generate()))

        p = fof.PredicateSignatureGenerator(arities=self.predicate_arities, functor_gen=f)
        print('predicates:', end=' ')
        pprint(list(p.generate()))

        a = fof.AtomSignatureGenerator(allowed_connectives=self.connectives, predicate_gen=p)
        print('atoms:', end=' ')
        pprint(list(a.generate()))

        l = fof.LiteralSignatureGenerator(atom_gen=a)
        print('literals:', end=' ')
        pprint(list(l.generate()))

        c = fof.CNFClauseSignatureGenerator(clause_lengths=self.clause_lengths, literal_gen=l)

        F = fof.CNFFormulaSignatureGenerator(clause_gen=c)
        gen = F.generate(
            number_of_clauses=self.number_of_clauses,
            number_of_literals=self.number_of_literals,
        )
        post_proc = FOLPostProcessor(predicate_names=self.predicate_names, functor_names=self.functor_names,
                                     variable_names=self.variable_names)

        for formula in gen:
            post_proc.switch_names(formula=formula)
            yield formula
