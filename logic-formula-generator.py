from __future__ import annotations

from ast.atom import Atom
from ast.cnf_clause import CNFClause
from ast.cnf_formula import CNFFormula
from ast.functor import Functor
from ast.literal import Literal
from ast.predicate import Predicate
from ast.variable import Variable

if __name__ == '__main__':
    v = Variable(name='V')
    x = Variable(name='X')
    f = Functor(name='f', terms=[v, x])

    # f.terms.append(deepcopy(f))
    p = Predicate(name='p', terms=[v, x, f])

    print('pred: ', str(p))
    print('functors: ', end='')
    for i in p.functors:
        print(str(i), end=' ')
    print('variables: ', end='')
    for i in p.variables:
        print(str(i), end=' ')

    a = Atom(connective='=', arguments=[p, p])
    print()
    print('atom: ')
    print(' terms: ', str(list(a.terms)))
    print(' predicates: ', str(list(a.predicates)))
    print(' functors: ', str(list(a.functors)))

    l = Literal(atom=a, negated=True)
    l2 = Literal(atom=Atom(connective='',
                           arguments=[Variable(name='G')]),
                 negated=True)
    print('literal: ', str(l))
    print('literal2: ', str(l2))

    c = CNFClause(literals=[l, l2])
    print('CNF clause: ', str(c))

    f = CNFFormula(clauses=[c])
    print('Formula: ', str(f))
