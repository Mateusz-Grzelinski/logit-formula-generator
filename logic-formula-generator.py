from __future__ import annotations

from src.ast.fol import Functor
from src.ast.fol.atom import Atom
from src.ast.fol.cnf_clause import CNFClause
from src.ast.fol.cnf_formula import CNFFormula
from src.ast.fol.literal import Literal
from src.ast.fol.predicate import Predicate
from src.ast.fol.variable import Variable

if __name__ == '__main__':
    v = Variable(name='V')
    x = Variable(name='X')
    f = Functor(name='f', items=[v, x])

    # f.terms.append(deepcopy(f))
    p = Predicate(name='p', items=[v, x, f])

    print('pred: ', str(p))
    print('functors: ', end='')
    for i in p.functors():
        print(str(i), end=' ')
    print('variables: ', end='')
    for i in p.variables():
        print(str(i), end=' ')

    a = Atom(connective='=', items=[p, p])
    print()
    print('atom: ')
    print(' terms: ', str(list(a.terms())))
    print(' predicates: ', str(list(a.predicates())))
    print(' functors: ', str(list(a.functors())))

    l = Literal(item=a, negated=True)
    l2 = Literal(item=Atom(connective='',
                           items=[Variable(name='G')]),
                 negated=True)
    print('literal: ', str(l))
    print('literal2: ', str(l2))

    c = CNFClause(items=[l, l2])
    print('CNF clause: ', str(c))

    f = CNFFormula(items=[c])
    print('Formula: ', str(f))
