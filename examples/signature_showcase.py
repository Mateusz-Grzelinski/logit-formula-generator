from pprint import pprint

import src.generators._signatures.first_order_logic as fol
from src.generators._range import IntegerRange

if __name__ == '__main__':
    f = fol.FunctorSignatureGenerator(arities=[0, 1], max_recursion_depth=0)
    print('functors:')
    pprint(list(f.generate()))

    p = fol.PredicateSignatureGenerator(arities=[0, 1], functor_gen=f)
    print('predicates:')
    pprint(list(p.generate()))

    a = fol.AtomSignatureGenerator(allowed_connectives={''}, predicate_gen=p)
    print('atoms:')
    pprint(list(a.generate()))

    l = fol.LiteralSignatureGenerator(atom_gen=a)
    print('literals:')
    pprint(list(l.generate()))

    c = fol.CNFClauseSignatureGenerator(clause_lengths={1, 3}, literal_gen=l)
    # print('clauses:')
    # pprint(list(c.generate()))

    F = fol.CNFFormulaSignatureGenerator(clause_gen=c)
    print('formulas:')
    gen = F.generate(
        number_of_clauses=IntegerRange(min=4, max=9),
        number_of_literals=IntegerRange(min=4, max=8),
    )
    for f in enumerate(gen):
        print(f)
        break
    # pprint(f'{next(gen)=}')
    # pprint(f'{next(gen)=}')
    # pprint(f'{next(gen)=}')

    # f1 = Functor('f', items=[Variable('V')])
    # f2 = Functor('f', items=[Variable('X')])
    # f = {f1, f2, }
    # print(f)